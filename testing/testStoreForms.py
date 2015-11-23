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

    def getDataFromResponse(self, resp):

            return json.loads(resp.content)

    def setUp(self):
        # Run first the setUp from the superclass
        self.factory = RequestFactory()
        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'MT',
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



    def testCreateStore(self):
        """
        Test creating one store
        """
        request = self.factory.post("/api/store/create", { 'username' : 'Tom',
                                             'name' : 'Great Stuff',
                                             'description' : 'Sells great stuff.',
                                             'phone_number' : '1234567890',
                                             'address_street' : 'this',
                                             'address_apt' : '',
                                             'address_city' : 'is',
                                             'address_state' : 'my',
                                             'address_zip' : 'address',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_store(request)
        self.assertRedirectResponse(response)

    def testCreateStoreUserDoesNotExist(self):
        """
        Test creating one store to a nonexistent user
        """
        request = self.factory.post("/api/store/create", { 'username' : 'Mack',
                                             'name' : 'Great Stuff',
                                             'description' : 'Sells great stuff.',
                                             'phone_number' : '1234567890',
                                             'address_street' : 'this',
                                             'address_apt' : '',
                                             'address_city' : 'is',
                                             'address_state' : 'my',
                                             'address_zip' : 'address',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_store(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)
        self.assertEquals([u'Username does not exist.'], resp['errors']['username'])

    def testCreateStoreEmptyFields(self):
        """
        Test creating one store with empty fields
        """
        request = self.factory.post("/api/store/create", { 'username' : 'Tom',
                                             })
        response = views.create_store(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)
        self.assertErrorRequired(resp['errors']['name'])



class TestEditStoreForms(TestCase):

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

    def getDataFromResponse(self, resp):

            return json.loads(resp.content)

    def setUp(self):
        # Run first the setUp from the superclass
        self.factory = RequestFactory()
        request = self.factory.post("/api/user/create", { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'MT',
                                             'email' : 'tommeng@berkeley.edu',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_user(request)
        self.assertRedirectResponse(response)
        request = self.factory.post("/api/store/create", { 'username' : 'Tom',
                                             'name' : 'Great Stuff',
                                             'description' : 'Sells great stuff.',
                                             'phone_number' : '1234567890',
                                             'address_street' : 'this',
                                             'address_apt' : '',
                                             'address_city' : 'is',
                                             'address_state' : 'my',
                                             'address_zip' : 'address',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_store(request)
        self.assertRedirectResponse(response)


    def tearDown(self):
        
        request = self.factory.post("/api/user/destroy", data={})
        response = views.empty_db(request)
        respDestroy = self.getDataFromResponse(response)
        self.assertSuccessResponse(respDestroy)


    def testCreateStoreDuplicate(self):
        """
        Test creating one store
        """
        request = self.factory.post("/api/store/create", { 'username' : 'Tom',
                                             'name' : 'Great Stuff',
                                             'description' : 'Sells great stuff.',
                                             'phone_number' : '1234567890',
                                             'address_street' : 'this',
                                             'address_apt' : '',
                                             'address_city' : 'is',
                                             'address_state' : 'my',
                                             'address_zip' : 'address',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.create_store(request)
        resp = self.getDataFromResponse(response)
        self.assertFailResponse(resp)
        self.assertEquals([u'Another store already exists at this address.'], resp['errors']['address'])

    def testEditStore(self):
        """
        Test editing one store
        """
        request = self.factory.post("/api/store/edit", { 'storeID' : 1,
                                             'name' : 'Great Stuff',
                                             'description' : 'Sells great stuff.',
                                             'phone_number' : '1234567890',
                                             'address_street' : 'this',
                                             'address_apt' : '',
                                             'address_city' : 'is',
                                             'address_state' : 'my',
                                             'address_zip' : 'address',
                                             'picture' : open('no-user-profile-picture.jpg'),
                                             })
        response = views.edit_store(request)
        self.assertRedirectResponse(response)

    # def testCreateStoreUserDoesNotExist(self):
    #     """
    #     Test creating one store to a nonexistent user
    #     """
    #     request = self.factory.post("/api/store/create", { 'username' : 'Mack',
    #                                          'name' : 'Great Stuff',
    #                                          'description' : 'Sells great stuff.',
    #                                          'phone_number' : '1234567890',
    #                                          'address_street' : 'this',
    #                                          'address_apt' : '',
    #                                          'address_city' : 'is',
    #                                          'address_state' : 'my',
    #                                          'address_zip' : 'address',
    #                                          'picture' : open('no-user-profile-picture.jpg'),
    #                                          })
    #     response = views.create_store(request)
    #     resp = self.getDataFromResponse(response)
    #     self.assertFailResponse(resp)
    #     self.assertEquals([u'Username does not exist.'], resp['errors']['username'])

    # def testCreateStoreEmptyFields(self):
    #     """
    #     Test creating one store with empty fields
    #     """
    #     request = self.factory.post("/api/store/create", { 'username' : 'Tom',
    #                                          })
    #     response = views.create_store(request)
    #     resp = self.getDataFromResponse(response)
    #     self.assertFailResponse(resp)
    #     self.assertErrorRequired(resp['errors']['name'])












