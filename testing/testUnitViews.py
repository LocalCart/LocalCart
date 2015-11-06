"""
This file contains a small subset of the tests we will run on your backend submission
"""

from django.test import TestCase
from django.test import RequestFactory
from LocalCartBack import views
from LocalCartBack import models
import json

import os
#import testLib

class TestUnitViewsCarts(TestCase):

    def assertSuccessResponse(self,
                              respData,
                              msg=None):
        """
        Check that the response is not an error response
        """
        self.assertEquals(200, respData['status'], msg)

    def assertFailResponse(self,
                              respData,
                              msg=None):
        self.assertEquals(400, respData['status'], msg)

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


 
    ###
    ### THESE ARE THE ACTUAL TESTS
    ###
    def testCreate1User(self):
        """
        Test adding one smile
        """
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request);
        respCreate = self.getDataFromResponse(response)

        self.assertSuccessResponse(respCreate)
        self.assertEquals("Tom", respCreate['username'], "Username wrong")
        self.assertEquals("customer", respCreate['user_type'])

    def testCreateUserWithEmptyUsername(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : '',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')

        response = views.create_user(request);
        respCreate = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreate)
        self.assertEquals("username must be non-empty", respCreate['errors'][0], "")

    def testCreateUserWithEmptyPassword(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')

        response = views.create_user(request);
        respCreate = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreate)
        self.assertEquals("password must be non-empty", respCreate['errors'][0], "")

    def testCreateUserWithInvalidUserType(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'student',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')

        response = views.create_user(request);
        respCreate = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreate)
        self.assertEquals("user_type must be either merchant or customer", respCreate['errors'][0], "") 



    def testEditUser(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')

        response = views.create_user(request);

        request = self.factory.post("/api/user/edit", json.dumps({ 'username' : 'Tom',
                                            'password' : '1234',
                                            'first_name': 'Tom',
                                            'last_name': 'Meng'}), content_type='application/json')
        response = views.edit_user(request)
        respEdit = self.getDataFromResponse(response)
        self.assertEquals("Tom", respEdit['first_name'])
        self.assertEquals("Meng", respEdit['last_name'])

    def testEditUserUsernameNotExist(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')

        response = views.create_user(request);

        request = self.factory.post("/api/user/edit", json.dumps({ 'username' : 'NotExist',
                                            'password' : '1234',
                                            'first_name': 'Tom',
                                            'last_name': 'Meng'}), content_type='application/json')
        response = views.edit_user(request)
        respEdit = self.getDataFromResponse(response)
        self.assertEquals("username does not exist", respEdit["errors"][0])

    def testEditUserEmptyField(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')

        response = views.create_user(request)

        request = self.factory.post("/api/user/edit", json.dumps({ 'username' : 'Tom',
                                            'password' : '',
                                            'first_name': '',
                                            'last_name': '',
                                            'email': ''}), content_type='application/json')
        response = views.edit_user(request)
        respEdit = self.getDataFromResponse(response)
        self.assertEquals("first_name must not be empty", respEdit["errors"][0])
        self.assertEquals("last_name must not be empty", respEdit["errors"][1])
        self.assertEquals("email must not be empty", respEdit["errors"][2])
        self.assertEquals("password must not be empty", respEdit["errors"][3])




    def testCreateStore(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreateStore)
        self.assertEquals(0, len(respCreateStore['errors']))

    def testCreateStoreUsernameNotExist(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'NotExist',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreateStore)
        self.assertEquals("username does not exist", respCreateStore['errors'][0])


    def testCreateStoreInvalidFields(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : '',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA',
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreateStore)
        self.assertEquals("address not correctly formatted", respCreateStore['errors'][0])
        self.assertEquals("name must be non-empty", respCreateStore['errors'][1])
        self.assertEquals("phone_number must be non-empty", respCreateStore['errors'][2])



# #################################################################################################
        

    def testCreateInventory(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : respCreateStore['storeID']
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreateInventory)
        self.assertEquals(0, len(respCreateInventory['errors']))

    def testCreateInventoryWithoutStoreID(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreateInventory)
        self.assertEquals("storeID must be an integer", respCreateInventory['errors'][0])

    def testCreateInventoryWithStoreIDNotExist(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : -1
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreateInventory)
        self.assertEquals("invalid storeID", respCreateInventory['errors'][0])

    def testCreateInventoryTwice(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : respCreateStore['storeID']
                                             }), content_type='application/json')
        response = views.create_inventory(request)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : respCreateStore['storeID']
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)  
        self.assertEquals("store already has an inventory", respCreateInventory['errors'][0])   

# ###################################################################################################
    def testCreateItem(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : respCreateStore['storeID']
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)


        request = self.factory.post("/api/inventory/add", json.dumps({ 'inventoryID' : respCreateInventory['inventoryID'],
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             }), content_type='application/json')
        response = views.create_item(request)
        respCreateItem = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreateItem)
        self.assertEquals(0, len(respCreateItem['errors']))


    def testCreateItemWithoutInventoryID(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : respCreateStore['storeID']
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)


        request = self.factory.post("/api/inventory/add", json.dumps({ 'inventoryID' : '',
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             }), content_type='application/json')
        response = views.create_item(request)
        respCreateItem = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreateItem)
        self.assertEquals("inventoryID must be an integer", respCreateItem['errors'][0]) 

    def testCreateItemWithInventoryIDNotExist(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : respCreateStore['storeID']
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)


        request = self.factory.post("/api/inventory/add", json.dumps({ 'inventoryID' : -1,
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             }), content_type='application/json')
        response = views.create_item(request)
        respCreateItem = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreateItem)
        self.assertEquals("invalid inventoryID", respCreateItem['errors'][0]) 

    def testCreateItemInvalidItemFields(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : respCreateStore['storeID']
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)


        request = self.factory.post("/api/inventory/add", json.dumps({ 'inventoryID' : respCreateInventory['inventoryID'],
                                             'name' : '',
                                             'picture': '',
                                             'price': '-2.00'
                                             }), content_type='application/json')
        response = views.create_item(request)
        respCreateItem = self.getDataFromResponse(response)
        self.assertSuccessResponse(respCreateItem)
        self.assertEquals("name must be non-empty", respCreateItem['errors'][0]) 
        self.assertEquals("description must be non-empty", respCreateItem['errors'][1]) 
        self.assertEquals("price must be a positive number", respCreateItem['errors'][2]) 
        self.assertEquals("picture must be non-empty", respCreateItem['errors'][3]) 


# #######################################################################################################

    def testEditItem(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : respCreateStore['storeID']
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)


        request = self.factory.post("/api/inventory/add", json.dumps({ 'inventoryID' : respCreateInventory['inventoryID'],
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             }), content_type='application/json')
        response = views.create_item(request)
        respCreateItem = self.getDataFromResponse(response)


        request = self.factory.post("/api/item/edit", json.dumps({ 'itemID' : respCreateItem['itemID'],
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '3.00'
                                             }), content_type='application/json')
        response = views.edit_item(request)
        respEditItem = self.getDataFromResponse(response)
        self.assertSuccessResponse(respEditItem)  
        self.assertEquals(0, len(respEditItem['errors']))


    def testEditItemWithoutItemID(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : respCreateStore['storeID']
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)


        request = self.factory.post("/api/inventory/add", json.dumps({ 'inventoryID' : respCreateInventory['inventoryID'],
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             }), content_type='application/json')
        response = views.create_item(request)
        respCreateItem = self.getDataFromResponse(response)


        request = self.factory.post("/api/item/edit", json.dumps({
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '3.00'
                                             }), content_type='application/json')
        response = views.edit_item(request)
        respEditItem = self.getDataFromResponse(response)
        self.assertSuccessResponse(respEditItem)  
        self.assertEquals("itemID must be an integer", respEditItem['errors'][0]) 

    def testEditItemWithItemIDNotExist(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : respCreateStore['storeID']
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)


        request = self.factory.post("/api/inventory/add", json.dumps({ 'inventoryID' : respCreateInventory['inventoryID'],
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             }), content_type='application/json')
        response = views.create_item(request)
        respCreateItem = self.getDataFromResponse(response)


        request = self.factory.post("/api/item/edit", json.dumps({ 'itemID' : -1,
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '3.00'
                                             }), content_type='application/json')
        response = views.edit_item(request)
        respEditItem = self.getDataFromResponse(response)
        self.assertSuccessResponse(respEditItem)  
        self.assertEquals("invalid itemID", respEditItem['errors'][0]) 



# ##############################################################################################################

#### This one is failing because don't know how to send a fake get request with json
    def testSearchItem(self):
        request = self.factory.get("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request)

        request = self.factory.post("/api/store/create", json.dumps({ 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\n \nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             }), content_type='application/json')
        response = views.create_store(request)
        respCreateStore = self.getDataFromResponse(response)

        request = self.factory.post("/api/inventory/create", json.dumps({ 'storeID' : respCreateStore['storeID']
                                             }), content_type='application/json')
        response = views.create_inventory(request)
        respCreateInventory = self.getDataFromResponse(response)


        request = self.factory.post("/api/inventory/add", json.dumps({ 'inventoryID' : respCreateInventory['inventoryID'],
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             }), content_type='application/json')
        response = views.create_item(request)

        request = self.factory.post("/api/search/items", json.dumps({ 'query' : 'apple','location' : '1234 12th st.\n \nBerkeley\nCA\n94704'}), content_type='application/json')
        response = views.search_items(request)
        respSearchItem = self.getDataFromResponse(response)


        self.assertSuccessResponse(respSearchItem)  
        #print len(respSearchItem['json_items'])
        self.assertEquals(0, len(respSearchItem['errors']))                        


#########################################################################################



    def testCreateList(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request);

        request = self.factory.post("/api/list/create", json.dumps({
                                             'username': 'Tom',
                                             'name': "Tom's shopping list"
                                             }), content_type='application/json')
        response = views.create_list(request)
        respCreateList = self.getDataFromResponse(response)

        self.assertEquals(0, len(respCreateList['errors']))    

    def testCreateListUsernameNotExist(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request);

        request = self.factory.post("/api/list/create", json.dumps({
                                             'username': 'NotExist',
                                             'name': "Tom's shopping list"
                                             }), content_type='application/json')
        response = views.create_list(request)
        respCreateList = self.getDataFromResponse(response)

        self.assertEquals("username does not exist or user is not a customer", respCreateList['errors'][0]) 

    def testCreateListUsernameNotCustomer(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'merchant',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request);

        request = self.factory.post("/api/list/create", json.dumps({
                                             'username': 'Tom',
                                             'name': "Tom's shopping list"
                                             }), content_type='application/json')
        response = views.create_list(request)
        respCreateList = self.getDataFromResponse(response)

        self.assertEquals("username does not exist or user is not a customer", respCreateList['errors'][0]) 

    def testCreateListInvalidFields(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request);

        request = self.factory.post("/api/list/create", json.dumps({
                                             'username': '',
                                             }), content_type='application/json')
        response = views.create_list(request)
        respCreateList = self.getDataFromResponse(response)

        self.assertEquals("username must be non-empty", respCreateList['errors'][0]) 
        self.assertEquals("name must be non-empty", respCreateList['errors'][1]) 


    def testDeleteList(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request);

        request = self.factory.post("/api/list/create", json.dumps({
                                             'username': 'Tom',
                                             'name': "Tom's shopping list"
                                             }), content_type='application/json')
        response = views.create_list(request)
        
        request = self.factory.post("/api/list/delete", json.dumps({
                                             'username': 'Tom',
                                             'name': "Tom's shopping list"
                                             }), content_type='application/json')
        response = views.delete_list(request)
        respDeleteList = self.getDataFromResponse(response)
        self.assertEquals(0, len(respDeleteList['errors']))  

    def testDeleteListUsernameNotExist(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request);

        request = self.factory.post("/api/list/create", json.dumps({
                                             'username': 'Tom',
                                             'name': "Tom's shopping list"
                                             }), content_type='application/json')
        response = views.create_list(request)
        
        request = self.factory.post("/api/list/delete", json.dumps({
                                             'username': 'NotExist',
                                             'name': "Tom's shopping list"
                                             }), content_type='application/json')
        response = views.delete_list(request)
        respDeleteList = self.getDataFromResponse(response)
        self.assertEquals("no list of this name exists for this username", respDeleteList['errors'][0])  

    def testDeleteListListnameNotExist(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request);

        request = self.factory.post("/api/list/create", json.dumps({
                                             'username': 'Tom',
                                             'name': "Tom's shopping list"
                                             }), content_type='application/json')
        response = views.create_list(request)
        
        request = self.factory.post("/api/list/delete", json.dumps({
                                             'username': 'Tom',
                                             'name': "NotExist"
                                             }), content_type='application/json')
        response = views.delete_list(request)
        respDeleteList = self.getDataFromResponse(response)
        self.assertEquals("no list of this name exists for this username", respDeleteList['errors'][0]) 

    def testDeleteListInvalidFields(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request);

        request = self.factory.post("/api/list/create", json.dumps({
                                             'username': 'Tom',
                                             'name': "Tom's shopping list"
                                             }), content_type='application/json')
        response = views.create_list(request)
        
        request = self.factory.post("/api/list/delete", json.dumps({
                                             'username': '',
                                             }), content_type='application/json')
        response = views.delete_list(request)
        respDeleteList = self.getDataFromResponse(response)
        self.assertEquals("username must be non-empty", respDeleteList['errors'][0]) 
        self.assertEquals("name must be non-empty", respDeleteList['errors'][1])   


    def testEditList(self):
        request = self.factory.post("/api/user/create", json.dumps({ 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu',
                                             }), content_type='application/json')
        response = views.create_user(request);

        request = self.factory.post("/api/list/create", json.dumps({
                                             'username': 'Tom',
                                             'name': "Tom's shopping list"
                                             }), content_type='application/json')
        response = views.create_list(request)
        respList = self.getDataFromResponse(response)

        request = self.factory.post("/api/list/edit", json.dumps({
                                             'listID': respList['listID'],
                                             'contents': [
                                                            {'name': 'chair', 'type': 'name'},
                                                            {'name': 'apple', 'type': 'name'}
                                                         ]
                                             }), content_type='application/json')
        response = views.edit_list(request)
        respEditList = self.getDataFromResponse(response)
        self.assertEquals(0, len(respEditList['errors']))  

    # def testLogin(self):
    #     request = self.factory.post("/api/user/login", json.dumps({ 'username' : 'Tom',
    #                                          'password' : '123456',
    #                                          'user_type' : 'customer',
    #                                          'email' : 'tommeng@berkeley.edu',
    #                                          }), content_type='application/json')

    #     response = views.create_user(request);
    #     respCreate = self.getDataFromResponse(response)
    #     self.assertSuccessResponse(respCreate)

    #     request = self.factory.post("/api/user/login", json.dumps({ 'username' : 'Tom',
    #                                          'password' : '123456'
    #                                          }), content_type='application/json')
    #     response = views.log_in(request)
    #     respLgoin = self.getDataFromResponse(response)
    #     self.assertSuccessResponse(respLogin)


    # def testLoginWrongPassword(self):
    #     request = self.factory.post("/api/user/login", json.dumps({ 'username' : 'Tom',
    #                                          'password' : '123456',
    #                                          'user_type' : 'customer',
    #                                          'email' : 'tommeng@berkeley.edu',
    #                                          }), content_type='application/json')

    #     response = views.create_user(request);
    #     respCreate = self.getDataFromResponse(response)
    #     self.assertSuccessResponse(respCreate)

    #     request = self.factory.post("/api/user/login", json.dumps({ 'username' : 'Tom',
    #                                          'password' : '1234'
    #                                          }), content_type='application/json')
    #     response = views.log_in(request)
    #     respLogin = self.getDataFromResponse(response)
    #     self.assertSuccessResponse(respLogin)
    #     self.assertEquals("invalid username and password combination", respLogin['errors'][0], "")








