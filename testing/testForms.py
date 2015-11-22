from django.test import TestCase
from django.test import RequestFactory
from LocalCartBack import views
from LocalCartBack import models
import json
import urllib
import os

class TestWithForms(TestCase):

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


