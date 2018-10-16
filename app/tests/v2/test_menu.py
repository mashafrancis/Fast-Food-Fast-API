import json
import unittest

from .base_test import BaseTests


class MenuTests(BaseTests):
    """Tests functionality of the menu endpoint"""

    def test_create_new_menu(self):
        """Test API can create an menu (POST)"""
        access_token = self.get_admin_token()

        response = self.client().post('/api/v2/menu', data=self.menu,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertTrue(data['message'] == u"A new menu has been added successfully.")
        self.assertFalse(data['message'] == u"Menu has been added successfully.")

    def test_get_all_menu(self):
        """Tests API can get all menu (GET)"""
        access_token = self.get_admin_token()

        # Test for no menu found.
        response = self.client().get('/api/v2/menu',
                                     headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"Sorry, No Menu found! Create one.")
        self.assertEqual(response.status_code, 404)
        self.assertNotEqual(response.status_code, 401)

        # Test user cannot delete non existent menu
        response = self.client().delete('/api/v2/menu',
                                        headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"There is no menu here!")
        self.assertEqual(response.status_code, 404)

        # Test for menu found.
        response = self.client().post('/api/v2/menu', data=self.menu,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/api/v2/menu',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)

    def test_delete_all_menu(self):
        """Test API can delete all menu (DELETE)"""
        access_token = self.get_admin_token()

        response = self.client().post('/api/v2/menu', data=self.menu,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)

        response = self.client().post('/api/v2/menu', data=self.menu2,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        # self.assertEqual(response.status_code, 201)

        response = self.client().delete('/api/v2/menu',
                                        headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'OK')
        self.assertEqual(data['message'], u"All menu has been successfully deleted!")
        self.assertEqual(response.status_code, 200)

    def test_get_menu_by_id(self):
        """Tests API can get one menu by using its id"""
        access_token = self.get_admin_token()

        # Test for no menu found.
        response = self.client().get('/api/v2/menu/20',
                                     headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"Sorry, Menu does't exist!")
        self.assertEqual(response.status_code, 404)

        # Test get menu by order_id
        response = self.client().post('/api/v2/menu', data=self.menu,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        response = self.client().get('/api/v2/menu/1',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Drinks', str(response.data))
        self.assertIn('Get your drinks!', str(response.data))

    def test_update_non_existing_menu(self):
        """Test updating an menu that does not exist"""
        access_token = self.get_admin_token()

        response = self.client().put('/api/v2/menu/1000', data=self.menu,
                                     content_type='application/json',
                                     headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 404)

    def test_menu_deletion(self):
        """Test API can delete and existing menu (DELETE)"""
        access_token = self.get_admin_token()

        # Test deleting non existing menu.
        response = self.client().delete('/api/v2/menu/10',
                                        headers=dict(Authorization="Bearer " + access_token))
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Not Found')
        self.assertEqual(data['message'], u"Sorry, No Menu found! Create one.")
        self.assertEqual(response.status_code, 404)

        response = self.client().post('/api/v2/menu', data=self.menu,
                                      content_type='application/json',
                                      headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 201)
        response = self.client().delete('/api/v2/menu/1',
                                        headers=dict(Authorization="Bearer " + access_token))

        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'OK')
        self.assertEqual(data['message'], u"Menu has been deleted!")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
