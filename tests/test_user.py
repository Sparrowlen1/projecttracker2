import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User('Levi', 'Levi@example.com', 'USR1')
        self.assertEqual(user.name, 'Levi')
        self.assertEqual(user.email, 'Levi@example.com')
        self.assertEqual(user.user_id, 'USR1')
    
    def test_user_to_dict(self):
        user = User('Ruth Mailu', 'Ruth Mailu@example.com', 'USR2')
        user_dict = user.to_dict()
        self.assertEqual(user_dict['name'], 'Ruth Mailu')
        self.assertEqual(user_dict['email'], 'Ruth Mailu@example.com')
    
    def test_user_from_dict(self):
        data = {'name': 'Daniel Muuo', 'email': 'daniel@example.com', 'user_id': 'USR3'}
        user = User.from_dict(data)
        self.assertEqual(user.name, 'Daniel Muuo')
        self.assertEqual(user.email, 'daniel@example.com')
    
    def test_display_info(self):
        user = User('Grace Mutee', 'grace@example.com', 'USR4')
        info = user.display_info()
        self.assertIn('Grace Mutee', info)
        self.assertIn('grace@example.com', info)

if __name__ == '__main__':
    unittest.main()