import json
import unittest

from .base_test import BaseTests


class OrderTests(BaseTests):
    """Tests functionality of the orders endpoint"""

    def test_create_order(self):
        """Test API can create an order (POST)"""
        with self.client():
            access_token = self.get_admin_token()

            self.client().post('/api/v2/menu', data=self.menu,
                               content_type='application/json',
                               headers=dict(Authorization="Bearer " + access_token))
            self.client().post('/api/v2/menu/1/meals', data=self.meal,
                               content_type='application/json',
                               headers=dict(Authorization="Bearer " + access_token))

            response = self.client().post('/api/v2/users/orders', data=self.order3,
                                          content_type='application/json',
                                          headers=dict(Authorization="Bearer " + access_token))
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data.decode())
            self.assertTrue(data['message'] == u"Order has been placed successfully.")

    def test_get_all_orders(self):
        """Tests API can get all orders (GET)"""
        with self.client():
            access_token = self.get_admin_token()
            self.create_menu(access_token)
            self.create_meal(access_token)

            response = self.client().post('/api/v2/users/orders', data=self.order3,
                                          content_type='application/json',
                                          headers=dict(Authorization="Bearer " + access_token))
            self.assertEqual(response.status_code, 201)
            response = self.client().get('/api/v2/users/orders',
                                         headers=dict(Authorization="Bearer " + access_token))
            self.assertEqual(response.status_code, 200)

    def test_get_no_orders(self):
        """Test for no orders found."""
        with self.client():
            access_token = self.get_admin_token()
            self.create_menu(access_token)
            self.create_meal(access_token)
            response = self.client().get('/api/v2/users/orders',
                                         headers=dict(Authorization="Bearer " + access_token))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Not Found')
            self.assertEqual(data['message'], u"You have not ordered any meal for a while. Place an order now?")
            self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_non_existent_orders(self):
        """Test user cannot delete non existent orders"""
        with self.client():
            access_token = self.get_admin_token()
            self.create_menu(access_token)
            self.create_meal(access_token)
            response = self.client().delete('/api/v2/users/orders',
                                            headers=dict(Authorization="Bearer " + access_token))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Not Found')
            self.assertEqual(data['message'], u"No orders available!")
            self.assertEqual(response.status_code, 404)

    def test_get_order_by_id(self):
        """Tests API can get one order by using its id"""
        with self.client():
            access_token = self.get_admin_token()
            self.create_menu(access_token)
            self.create_meal(access_token)
            response = self.client().post('/api/v2/users/orders', data=self.order3,
                                          content_type='application/json',
                                          headers=dict(Authorization="Bearer " + access_token))
            self.assertEqual(response.status_code, 201)
            response = self.client().get('/api/v2/orders/1',
                                         headers=dict(Authorization="Bearer " + access_token))
            self.assertEqual(response.status_code, 200)
            self.assertIn('Burger', str(response.data))

    def test_cannot_get_non_existing_order_by_id(self):
        """Tests API cannot get a non existing order by using its id"""
        with self.client():
            access_token = self.get_admin_token()
            self.create_menu(access_token)
            self.create_meal(access_token)
            response = self.client().get('/api/v2/orders/2',
                                         headers=dict(Authorization="Bearer " + access_token))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Not Found')
            self.assertEqual(data['message'], u"Sorry, Order No 2 does't exist!")
            self.assertEqual(response.status_code, 404)

    def test_update_non_existing_order(self):
        """Test updating an order that does not exist"""
        with self.client():
            access_token = self.get_admin_token()
            response = self.client().put('/api/v2/orders/100', data=self.update_order,
                                         content_type='application/json',
                                         headers=dict(Authorization="Bearer " + access_token))
            self.assertEqual(response.status_code, 404)

    def test_delete_all_orders(self):
        """Test API can delete all orders (DELETE)"""
        with self.client():
            access_token = self.get_admin_token()
            self.create_menu(access_token)
            self.create_meal(access_token)
            response = self.client().post('/api/v2/users/orders', data=self.order3,
                                          content_type='application/json',
                                             headers=dict(Authorization="Bearer " + access_token))
            self.assertEqual(response.status_code, 201)

            response = self.client().delete('/api/v2/orders',
                                            headers=dict(Authorization="Bearer " + access_token))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'OK')
            self.assertEqual(data['message'], u"All orders have been successfully deleted!")
            self.assertEqual(response.status_code, 200)

    def test_order_deletion(self):
        """Test API can delete and existing order (DELETE)"""
        with self.client():
            access_token = self.get_admin_token()
            self.create_menu(access_token)
            self.create_meal(access_token)

            # Test deleting non existing order.
            response = self.client().delete('/api/v2/orders/10',
                                            headers=dict(Authorization="Bearer " + access_token))
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'Not Found')
            self.assertEqual(data['message'], u"Order No 10 does not exist!")
            self.assertEqual(response.status_code, 404)

            response = self.client().post('/api/v2/users/orders', data=self.order3,
                                          content_type='application/json',
                                          headers=dict(Authorization="Bearer " + access_token))
            self.assertEqual(response.status_code, 201)
            response = self.client().delete('/api/v2/orders/1',
                                            headers=dict(Authorization="Bearer " + access_token))

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'OK')
            self.assertEqual(data['message'], u"Order No 1 has been deleted!")
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
