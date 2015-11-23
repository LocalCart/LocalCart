from django.test import TestCase
from django.test import RequestFactory
from LocalCartBack import views
from LocalCartBack import models
import json
import urllib
import os

class TestNewStoreForms(TestCase):

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
