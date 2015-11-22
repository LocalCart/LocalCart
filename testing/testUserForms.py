from django.test import TestCase
from django.test import RequestFactory
from LocalCartBack import views
from LocalCartBack import models
import json
import urllib
import os

class TestNewUserForms(TestCase):

    def assertSuccessResponse(self, resp, msg=None):
        """
        Check that the response is not an error response
        """
        self.assertEquals(200, resp['status'], msg)
        self.assertTrue(len(resp['errors']) == 0)

    def assertFailResponse(self, resp, msg=None):
        self.assertEquals(200, resp['status'], msg)
        self.assertTrue(len(resp['errors']) > 0)

    def assertRedirectResponse(self, resp, msg=None):
        self.assertEquals(302, resp.status_code, msg)

    def assertErrorRequired(self, resp, msg=None):
        self.assertEquals([u'This field is required.'], resp, msg)

    def assertErrorInvalidChoice(self, invalid, resp, msg=None):
        self.assertEquals([u'Select a valid choice. ' + invalid + ' is not one of the available choices.'], resp, msg)

    def assertErrorInvalidEmail(self, resp, msg=None):
        self.assertEquals([u'Enter a valid email address.'], resp, msg)

    def getDataFromResponse(self, resp):

            return json.loads(resp.content)

    def setUp(self):
        # Run first the setUp from the superclass
        self.factory = RequestFactory()

    def tearDown(self):
        
        request = self.factory.post("/api/user/destroy", data={})
        response = views.empty_db(request)
        respDestroy = self.getDataFromResponse(response)
        self.assertSuccessResponse(respDestroy)



    def testCreate1User(self):
        """
        Test adding one user
        """
        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'CR',
                                             'email' : 'tommeng@berkeley.edu',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_user(request)
        self.assertRedirectResponse(response)

    def testCreateUserNoPicture(self):
        """
        Test adding one user without picture
        """
        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'CR',
                                             'email' : 'tommeng@berkeley.edu',
                                             })
        response = views.create_user(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)

    def testCreateUserNoUsername(self):
        """
        Test adding one user without username
        """
        request = self.factory.post("/api/user/create", { 'username' : '',
                                             'password' : '123456',
                                             'user_type' : 'CR',
                                             'email' : 'tommeng@berkeley.edu',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_user(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)
        self.assertErrorRequired(resp['errors']['username'])

    def testCreateUserNoPassword(self):
        """
        Test adding one user without password
        """
        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '',
                                             'user_type' : 'CR',
                                             'email' : 'tommeng@berkeley.edu',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_user(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)
        self.assertErrorRequired(resp['errors']['password'])

    def testCreateUserNoUserType(self):
        """
        Test adding one user without user type
        """
        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : '',
                                             'email' : 'tommeng@berkeley.edu',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_user(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)
        self.assertErrorRequired(resp['errors']['user_type'])

    def testCreateUserInvalidUserType(self):
        """
        Test adding one user with invalid user type
        """
        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'cute',
                                             'email' : 'tommeng@berkeley.edu',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_user(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)
        self.assertErrorInvalidChoice('cute', resp['errors']['user_type'])

    def testCreateUserNoEmail(self):
        """
        Test adding one user without email
        """
        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'CR',
                                             'email' : '',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_user(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)
        self.assertErrorRequired(resp['errors']['email'])

    def testCreateUserInvalidEmail(self):
        """
        Test adding one user with invalid email
        """
        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'CR',
                                             'email' : 'tommengberkeley.edu',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_user(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)
        self.assertErrorInvalidEmail(resp['errors']['email'])

    def testCreateUserUsernameTaken(self):
        """
        Test adding two users with same username
        """
        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'CR',
                                             'email' : 'tommeng@berkeley.edu',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_user(request)
        self.assertRedirectResponse(response)

        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'CR',
                                             'email' : 'tommeng@berkeley.edu',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_user(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)
        self.assertEquals([u'Username already exists.'], resp['errors']['username'])


class TestEditUserForms(TestCase):

    def assertSuccessResponse(self,
                              resp,
                              msg=None):
        """
        Check that the response is not an error response
        """
        self.assertEquals(200, resp['status'], msg)

    def assertFailResponse(self,
                              resp,
                              msg=None):
        self.assertEquals(200, resp['status'], msg)
        self.assertTrue(len(resp['errors']) > 0)

    def assertRedirectResponse(self,
                              resp,
                              msg=None):
        self.assertEquals(302, resp.status_code, msg)

    def assertErrorInvalidEmail(self, resp, msg=None):
        self.assertEquals([u'Enter a valid email address.'], resp, msg)
        
    def getDataFromResponse(self, resp):

            return json.loads(resp.content)

    def setUp(self):
        # Run first the setUp from the superclass
        self.factory = RequestFactory()
        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'CR',
                                             'email' : 'tommeng@berkeley.edu',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_user(request)
        self.assertRedirectResponse(response)

    def tearDown(self):
        
        request = self.factory.post("/api/user/destroy", data={})
        response = views.empty_db(request)
        respDestroy = self.getDataFromResponse(response)
        self.assertSuccessResponse(respDestroy)

    def testEditUserEmpty(self):
        """
        Test edit Tom with empty parameters
        """
        request = self.factory.post("/api/user/edit", { 'username' : 'Tom',
                                             })
        response = views.edit_user(request)
        self.assertRedirectResponse(response)

    def testEditUserInvalidEmail(self):
        """
        Test edit Tom with empty parameters
        """
        request = self.factory.post("/api/user/edit", { 'username' : 'Tom',
                                             'email' : 'tommengberkeley.edu',
                                             })
        response = views.edit_user(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)
        self.assertErrorInvalidEmail(resp['errors']['email'])













