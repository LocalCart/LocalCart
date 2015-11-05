from django.test import TestCase
from LocalCartBack import models

"""
To test all tests: ./manage.py test
To test specific file: ./manage.py test testing.file_name
"""


class UserInfoTestCase(TestCase):

	def test_create_new_user(self):
		# Create a customer user.
		username = "Linda"
		password = "123"
		email = "rlzhang@berkeley.edu"
		user_type = "customer"
		picture = 'images/default_user_image'
		new_user_info = models.create_new_user(username=username, password=password, email=email, 
			first_name='', last_name='', user_type=user_type, picture=picture)
		self.assertEqual(new_user_info.user.username, username)
		self.assertEqual(new_user_info.user.email, email)
		self.assertEqual(new_user_info.user.first_name, '')
		self.assertEqual(new_user_info.user.last_name, '')
		self.assertEqual(new_user_info.user_type, user_type)
		self.assertEqual(new_user_info.picture, picture)
