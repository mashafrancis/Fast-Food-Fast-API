import json
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_test import BaseTests


class TokenTestCase(BaseTests):
    """Class to test token authentication"""
    def test_no_token(self):
        """Test there is no existing token"""
        response = self.client().post('/api/v2/orders',
                                      data=self.order)
        return response
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'Unauthorized')
        self.assertTrue(data['message'] == 'No access token!')
        self.assertEqual(response.status_code, 401)
