from django.test import TestCase
from LocalCartBack import models
from django.contrib.auth import authenticate

"""
To test all tests: ./manage.py test
To test specific file: ./manage.py test testing.file_name
"""

class CustomerMocker:

	def create_customer_user_Linda(self):
		# Creates customer Linda.
		username = "Linda"
		password = "123"
		email = "funfunfunfunfunfunfun@gmail.com"
		user_type = "customer"
		picture = 'images/default_user_image'
		new_user_info = models.UserInfo.create_new_user(username=username, password=password, email=email, 
			first_name='', last_name='', user_type=user_type, picture=picture)
		return new_user_info

	def create_customer_user_Ruth(self):
		# Creates customer Linda.
		username = "Ruth"
		password = "123"
		email = "rlzhang@berkeley.edu"
		user_type = "customer"
		picture = 'images/default_user_image'
		new_user_info = models.UserInfo.create_new_user(username=username, password=password, email=email, 
			first_name='', last_name='', user_type=user_type, picture=picture)
		return new_user_info

class UserInfoTestCase(TestCase):

	def test_create_new_user(self):
		# Create a customer user.
		username = "Linda"
		password = "123"
		email = "rlzhang@berkeley.edu"
		user_type = "customer"
		picture = 'images/default_user_image'
		new_user_info = models.UserInfo.create_new_user(username=username, password=password, email=email, 
			first_name='', last_name='', user_type=user_type, picture=picture)
		self.assertEqual(new_user_info.user.username, username)
		self.assertEqual(new_user_info.user.email, email)
		self.assertEqual(new_user_info.user.first_name, '')
		self.assertEqual(new_user_info.user.last_name, '')
		self.assertEqual(new_user_info.user_type, user_type)
		self.assertEqual(new_user_info.picture, picture)
		self.assertTrue(authenticate(username=username, password=password))

	def test_create_two_same_users(self):
		# Check that you cannot create two users of the same username.
		customer = CustomerMocker()
		original_user = customer.create_customer_user_Linda()
		duplicate_user = customer.create_customer_user_Linda()
		self.assertTrue(original_user)
		self.assertEqual(duplicate_user, None)

	def test_edit_user_info(self):
		# Edit Linda's info.
		customer = CustomerMocker()
		user = customer.create_customer_user_Linda()
		first_name = "Linda"
		last_name = "Zhang"
		email = "r.linda.zhang@gmail.com"
		password = "987"
		picture = 'prettybirdies'
		edited_user_type = models.UserInfo.edit_user_info(username=user.user.username)
		self.assertEqual(edited_user_type, user.user_type)
		edited_user_type = models.UserInfo.edit_user_info(username=user.user.username, first_name=first_name, last_name=last_name,
			email=email, password=password, picture=picture)
		self.assertEqual(edited_user_type, user.user_type)
		user = models.UserInfo.objects.get(user__username=user.user.username)
		self.assertEqual(user.user.first_name, first_name)
		self.assertEqual(user.user.last_name, last_name)
		self.assertEqual(user.picture, picture)
		self.assertTrue(authenticate(username=user.user.username, password=password))

	def test_edit_user_info_nonexistent(self):
		# Try to edit non-existent user.
		edited_user_type = models.UserInfo.edit_user_info(username="Leila")
		self.assertEqual(edited_user_type, None)
