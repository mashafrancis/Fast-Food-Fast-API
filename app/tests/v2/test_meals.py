import json
import unittest

from .base_test import BaseTests


class MealTests(BaseTests):
    """Tests functionality of the meal endpoint"""

    def test_create_new_meal(self):
        """Test API can create an meal (POST)"""
        access_token = self.user_token_get()
        self.create_menu(access_token)

        response = self.client().post('/api/v2/menu/1/meals', data=self.meal,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        # self.assertIn('Burger', str(response.data))
        self.assertTrue(data['message'] == u"A new meal has been offered.")
        self.assertFalse(data['message'] == u"Meal has been offered.")

        # Test duplicate meal addition
        response2 = self.client().post('/api/v2/menu/1/meals', data=self.meal,
                                       content_type='application/json',
                                       headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response2.status_code, 409)
        # self.assertTrue(data['message'] == u"You can not add the same meal item twice. Do you want to update?")
        self.assertFalse(data['message'] == u"You can not add the meal item.")

        # Test multiple meal creation in one menu
        response3 = self.client().post('/api/v2/menu/1/meals', data=self.meal2,
                                       content_type='application/json',
                                       headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response3.status_code, 201)
        # self.assertIn('Burger-2', str(response3.data))
        self.assertTrue(data['message'] == u"A new meal has been offered.")

    def test_new_meal_must_be_created_in_a_menu(self):
        """Test API must create a new meal in a menu. (POST)"""
        access_token = self.user_token_get()

        response = self.client().post('/api/v2/menu/1/meals', data=self.meal,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)
        self.assertNotIn('Burger-1', str(response.data))

    def test_get_all_meals(self):
        """Tests API can get all meals (GET)"""
        access_token = self.user_token_get()
        self.create_menu(access_token)

        # Test for no meal found.
        response = self.client().get('/api/v2/menu/1/meals',
                                     headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"Sorry, No Meal found!")
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 401)

        # Test admin cannot delete non existent meal
        response = self.client().delete('/api/v2/menu/1/meals',
                                        headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"There is no meal here!")
        self.assertEqual(response.status_code, 404)

        # Test for meal found.
        response = self.client().post('/api/v2/menu/1/meals', data=self.meal,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/api/v2/menu/1/meals',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)

    def test_delete_all_meals(self):
        """Test API can delete all meals (DELETE)"""
        access_token = self.user_token_get()
        self.create_menu(access_token)

        response = self.client().post('/api/v2/menu/1/meals', data=self.meal,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)

        response = self.client().post('/api/v2/menu/1/meals', data=self.meal2,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)

        response = self.client().delete('/api/v2/menu/1/meals',
                                        headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'OK')
        self.assertEqual(data['message'], u"Meals have been successfully deleted!")
        self.assertEqual(response.status_code, 200)

    def test_get_meal_by_id(self):
        """Tests API can get one meal by using its id"""
        access_token = self.user_token_get()
        self.create_menu(access_token)

        # Test for no meal found.
        response = self.client().get('/api/v2/menu/1/meals/100',
                                     headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"Sorry, Meal does't exist! Create one?")
        self.assertEqual(response.status_code, 404)

        # Test get meal by meal_id
        response2 = self.client().post('/api/v2/menu/1/meals', data=self.meal,
                                       content_type='application/json',
                                       headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response2.status_code, 201)
        response3 = self.client().get('/api/v2/menu/1/meals/1',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response3.status_code, 200)
        self.assertIn('Burger', str(response3.data))
        self.assertIn('Get your burger!', str(response3.data))

    def test_update_non_existing_order(self):
        """Test updating an meal that does not exist"""
        access_token = self.user_token_get()
        self.create_menu(access_token)

        response = self.client().put('/api/v2/menu/1/meals/100', data=self.meal2,
                                     content_type='application/json',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)

    def test_meals_deletion(self):
        """Test API can delete and existing meal (DELETE)"""
        access_token = self.user_token_get()
        self.create_menu(access_token)

        # Test deleting non existing meal.
        response = self.client().delete('/api/v2/menu/1/meals/100',
                                        headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"Sorry, No Meal found!")
        self.assertEqual(response.status_code, 404)

        response = self.client().post('/api/v2/menu/1/meals', data=self.meal,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        response = self.client().delete('/api/v2/menu/1/meals/1',
                                        headers=dict(Authorization="Bearer " + access_token))

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'OK')
        self.assertEqual(data['message'], u"Meal has been deleted!")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
