from django.test import TestCase
from LocalCartBack import models, views
from django.http import QueryDict
import json

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




