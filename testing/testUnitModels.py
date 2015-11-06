from django.test import TestCase
from LocalCartBack import models, views
from django.http import QueryDict
import json
from django.contrib.auth import authenticate

"""
To test all tests: ./manage.py test
To test specific file: ./manage.py test testing.file_name
"""

class ViewHelperTestCase(TestCase):

    def test_check_empty(self):
        fields = ['a', 'b']
        post = QueryDict('', mutable=True)
        body = '''
              {
               "a": "test",
               "b": "test"
              }
              '''
        post.update(json.loads(body))
        errors = views.check_empty(fields, post, [])
        self.assertTrue(len(errors) ==  0)

    def test_check_empty_missing(self):
        fields = ['a', 'b']
        post = QueryDict('', mutable=True)
        body = '''
              {
               "a": "test"
              }
              '''
        post.update(json.loads(body))
        errors = views.check_empty(fields, post, [])
        self.assertTrue(len(errors) >= 1)
        post = QueryDict('', mutable=True)
        body = '''
              {
               "a": "test",
               "b": ""
              }
              '''
        post.update(json.loads(body))
        errors = views.check_empty(fields, post, [])
        self.assertTrue(len(errors) >= 1)




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
		# Creates customer Ruth.
		username = "Ruth"
		password = "123"
		email = "rlzhang@berkeley.edu"
		user_type = "customer"
		picture = 'images/default_user_image'
		new_user_info = models.UserInfo.create_new_user(username=username, password=password, email=email, 
			first_name='', last_name='', user_type=user_type, picture=picture)
		return new_user_info

class MerchantMocker:

	def create_merchant_user_Leila(self):
		# Create merchant Leila.
		username = "Leila"
		password = "123"
		email = "leilaiscool@gmail.com"
		user_type = "merchant"
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
		edited_user_info = models.UserInfo.edit_user_info(username=user.user.username)
		self.assertEqual(edited_user_info.user_type, user.user_type)
		edited_user_type = models.UserInfo.edit_user_info(username=user.user.username, first_name=first_name, last_name=last_name,
			email=email, password=password, picture=picture)
		self.assertEqual(edited_user_info.user_type, user.user_type)
		user = models.UserInfo.objects.get(user__username=user.user.username)
		self.assertEqual(user.user.first_name, first_name)
		self.assertEqual(user.user.last_name, last_name)
		self.assertEqual(user.picture, picture)
		self.assertTrue(authenticate(username=user.user.username, password=password))

	def test_edit_user_info_nonexistent(self):
		# Try to edit non-existent user.
		edited_user_type = models.UserInfo.edit_user_info(username="Leila")
		self.assertEqual(edited_user_type, None)

class StoreTestCase(TestCase):

	def test_create_new_store(self):
		# Create new store with all correct info.
		merchant = MerchantMocker()
		user = merchant.create_merchant_user_Leila()
		name = "Unique Unicorns"
		description = "A place where only the magical ponies can play."
		picture = 'ofcourseofunicorns'
		address_street = '777 Rainbow Road'
		address_city = 'Unicorn City'
		address_state = 'Clouds'
		address_zip = '12345'
		phone_number = '1234567890'
		new_store = models.Store.create_new_store(user=user.user, name=name, description=description, picture=picture,
                          address_street=address_street, address_city=address_city,
                          address_state = address_state, address_zip = address_zip,
                          phone_number=phone_number)
		self.assertEqual(new_store.user, user.user)
		self.assertEqual(new_store.name, name)
		self.assertEqual(new_store.description, description)
		self.assertEqual(new_store.picture, picture)
		self.assertEqual(new_store.address_street, address_street)
		self.assertEqual(new_store.address_city, address_city)
		self.assertEqual(new_store.address_state, address_state)
		self.assertEqual(new_store.address_zip, address_zip)
		self.assertEqual(new_store.phone_number, phone_number)

