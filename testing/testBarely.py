"""
This file contains a small subset of the tests we will run on your backend submission
"""

import unittest
import os
import testLib

class TestCarts(testLib.CartTestCase):

    def tearDown(self):
        respDestroy = self.makeRequest("/api/user/destroy", method="POST",
                                    data = {})
        self.assertSuccessResponse(respDestroy)
    ###
    ### THESE ARE THE ACTUAL TESTS
    ###
    def testCreate1User(self):
        """
        Test adding one smile
        """
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertSuccessResponse(respCreate)
        self.assertEquals("Tom", respCreate['username'], "Username wrong")
        self.assertEquals("customer", respCreate['user_type'])

    def testCreateUserWithEmptyUsername(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : '',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertFailResponse(respCreate)
        self.assertEquals("username must be non-empty", respCreate['errors'][0], "")

    def testCreateUserWithEmptyPassword(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertFailResponse(respCreate)
        self.assertEquals("password must be non-empty", respCreate['errors'][0], "")

    def testCreateUserWithInvalidUserType(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'student',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertFailResponse(respCreate)
        self.assertEquals("user_type must be either merchant or customer", respCreate['errors'][0], "") 


    def testLogin(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })
        self.assertSuccessResponse(respCreate)
        respLogin = self.makeRequest("/api/user/login", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456'
                                             })
        self.assertSuccessResponse(respLogin)
        self.assertEquals("invalid username and password combination", respLogin['errors'][0], "")
        ################################# this is not correct yet###########################


    def testLoginWrongPassword(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })
        self.assertSuccessResponse(respCreate)
        respLogin = self.makeRequest("/api/user/login", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '1234'
                                             })
        self.assertSuccessResponse(respLogin)
        self.assertEquals("invalid username and password combination", respLogin['errors'][0], "")


    def testCreateStore(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertSuccessResponse(respCreate)

        respCreateStore = self.makeRequest("/api/store/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             })

        self.assertSuccessResponse(respCreateStore)

    def testCreateInventory(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertSuccessResponse(respCreate)

        respCreateStore = self.makeRequest("/api/store/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000'
                                             })
        self.assertSuccessResponse(respCreateStore)

        respCreateInventory = self.makeRequest("/api/inventory/create", method="POST",
                                    data = { 'storeID' : respCreateStore['storeID']
                                             })
        self.assertSuccessResponse(respCreateInventory)




    def testCreateItem(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertSuccessResponse(respCreate)

        respCreateStore = self.makeRequest("/api/store/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000'
                                             })
        self.assertSuccessResponse(respCreateStore)

        respCreateInventory = self.makeRequest("/api/inventory/create", method="POST",
                                    data = { 'storeID' : respCreateStore['storeID']
                                             })
        self.assertSuccessResponse(respCreateInventory)

        respCreateItem = self.makeRequest("/api/inventory/add", method="POST",
                                    data = { 'inventoryID' : respCreateInventory['inventoryID'],
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             })
        self.assertSuccessResponse(respCreateItem)

    def testEditItem(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertSuccessResponse(respCreate)

        respCreateStore = self.makeRequest("/api/store/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000'
                                             })
        self.assertSuccessResponse(respCreateStore)

        respCreateInventory = self.makeRequest("/api/inventory/create", method="POST",
                                    data = { 'storeID' : respCreateStore['storeID']
                                             })
        self.assertSuccessResponse(respCreateInventory)

        respCreateItem = self.makeRequest("/api/inventory/add", method="POST",
                                    data = { 'inventoryID' : respCreateInventory['inventoryID'],
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             })
        self.assertSuccessResponse(respCreateItem)

        respEditItem = self.makeRequest("/api/item/edit", method="POST",
                                    data = { 'itemID' : respCreateItem['itemID'],
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '3.00'
                                             })
        self.assertSuccessResponse(respEditItem)    

    def testSearchItem(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertSuccessResponse(respCreate)

        respCreateStore = self.makeRequest("/api/store/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'name' : 'Tom store',
                                             'address' : '1234 12th st.\nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000'
                                             })
        self.assertSuccessResponse(respCreateStore)

        respCreateInventory = self.makeRequest("/api/inventory/create", method="POST",
                                    data = { 'storeID' : respCreateStore['storeID']
                                             })
        self.assertSuccessResponse(respCreateInventory)

        respCreateItem = self.makeRequest("/api/inventory/add", method="POST",
                                    data = { 'inventoryID' : respCreateInventory['inventoryID'],
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             })
        self.assertSuccessResponse(respCreateItem)

        respSearchItem = self.makeRequest("/api/search/items", method="GET",
                                    data = { 'query' : 'apple',
                                             'location' : 'a\n1234 12th st.\nBerkeley\nCA\n94704',
                                             })    

        self.assertSuccessResponse(respSearchItem)                                      








