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

        self.assertSuccessResponse(respCreate)
        self.assertEquals("username must be non-empty", respCreate['errors'][0], "")

    def testCreateUserWithEmptyPassword(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertSuccessResponse(respCreate)
        self.assertEquals("password must be non-empty", respCreate['errors'][0], "")

    def testCreateUserWithInvalidUserType(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'student',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertSuccessResponse(respCreate)
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
        self.assertFailResponse(respLogin)
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

    # def testCreateStoreNoUserName(self):
    #     respCreate = self.makeRequest("/api/user/create", method="POST",
    #                                 data = { 'username' : 'Tom',
    #                                          'password' : '123456',
    #                                          'user_type' : 'customer',
    #                                          'email' : 'tommeng@berkeley.edu'
    #                                          })

    #     self.assertSuccessResponse(respCreate)

    #     respCreateStore = self.makeRequest("/api/store/create", method="POST",
    #                                 data = { 'username' : '',
    #                                          'name' : 'Tom Store',
    #                                          'address' : '1234 12th st.\nBerkeley\nCA\n94704',
    #                                          'phone_number' : '(510)642-6000',
    #                                          #'picture' : 'pic',
    #                                          #'description' : 'This is a very good store'
    #                                          })
    #     self.assertFailResponse(respCreateStore)

    # def testCreateStoreUserNameNotExist(self):
    #     respCreate = self.makeRequest("/api/user/create", method="POST",
    #                                 data = { 'username' : 'Tom',
    #                                          'password' : '123456',
    #                                          'user_type' : 'customer',
    #                                          'email' : 'tommeng@berkeley.edu'
    #                                          })

    #     self.assertSuccessResponse(respCreate)

    #     respCreateStore = self.makeRequest("/api/store/create", method="POST",
    #                                 data = { 'username' : 'T',
    #                                          'name' : 'Tom Store',
    #                                          'address' : '1234 12th st.\nBerkeley\nCA\n94704',
    #                                          'phone_number' : '(510)642-6000',
    #                                          #'picture' : 'pic',
    #                                          #'description' : 'This is a very good store'
    #                                          })
    #     self.assertFailResponse(respCreateStore)


    def testCreateStoreNoName(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertSuccessResponse(respCreate)

        respCreateStore = self.makeRequest("/api/store/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'name' : '',
                                             'address' : '1234 12th st.\nBerkeley\nCA\n94704',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             })
        self.assertFailResponse(respCreateStore)



    def testCreateStoreNoAddress(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertSuccessResponse(respCreate)

        respCreateStore = self.makeRequest("/api/store/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'name' : 'Tom Store',
                                             'address' : '',
                                             'phone_number' : '(510)642-6000',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             })
        self.assertFailResponse(respCreateStore)

    def testCreateStoreNoPhoneNumber(self):
        respCreate = self.makeRequest("/api/user/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'password' : '123456',
                                             'user_type' : 'customer',
                                             'email' : 'tommeng@berkeley.edu'
                                             })

        self.assertSuccessResponse(respCreate)

        respCreateStore = self.makeRequest("/api/store/create", method="POST",
                                    data = { 'username' : 'Tom',
                                             'name' : '',
                                             'address' : '1234 12th st.\nBerkeley\nCA\n94704',
                                             'phone_number' : '',
                                             #'picture' : 'pic',
                                             #'description' : 'This is a very good store'
                                             })
        self.assertFailResponse(respCreateStore)


#################################################################################################
        

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

    def testCreateInventoryWithoutStoreID(self):
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
                                    data = { 'storeID' : ''                                             })
        self.assertFailResponse(respCreateInventory)

    def testCreateInventoryWithStoreIDNotExist(self):
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
                                    data = { 'storeID' : '100'
                                             })
        self.assertFailResponse(respCreateInventory)

###################################################################################################
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


    def testCreateItemWithoutInventoryID(self):
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
                                    data = { 'inventoryID' : '',
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             })
        self.assertFailResponse(respCreateItem)

    def testCreateItemWithInventoryIDNotExist(self):
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
                                    data = { 'inventoryID' : '100',
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             })
        self.assertFailResponse(respCreateItem)

    def testCreateItemWithoutName(self):
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
                                             'name' : '',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             })
        self.assertFailResponse(respCreateItem)

    def testCreateItemWithoutDescription(self):
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
                                             'description': '',
                                             'picture': 'the picture',
                                             'price': '2.00'
                                             })
        self.assertFailResponse(respCreateItem)

    def testCreateItemWithoutPicture(self):
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
                                             'picture': '',
                                             'price': '2.00'
                                             })
        self.assertFailResponse(respCreateItem)

    def testCreateItemWithoutPrice(self):
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
                                             'price': ''
                                             })
        self.assertFailResponse(respCreateItem)


#######################################################################################################

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

    def testEditItemWithoutItemID(self):
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
                                    data = { 'itemID' : '',
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '3.00'
                                             })
        self.assertFailResponse(respEditItem)    

    def testEditItemWithItemIDNotExist(self):
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
                                    data = { 'itemID' : '100',
                                             'name' : 'apple',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '3.00'
                                             })
        self.assertFailResponse(respEditItem)  


    def testEditItemWithoutName(self):
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
                                             'name' : '',
                                             'description': 'Fuji',
                                             'picture': 'the picture',
                                             'price': '3.00'
                                             })
        self.assertSuccessResponse(respEditItem)  

    def testEditItemWithoutDescription(self):
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
                                             'description': '',
                                             'picture': 'the picture',
                                             'price': '3.00'
                                             })
        self.assertSuccessResponse(respEditItem)  

    def testEditItemWithoutPicture(self):
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
                                             'picture': '',
                                             'price': '3.00'
                                             })
        self.assertSuccessResponse(respEditItem)  

    def testEditItemWithoutPrice(self):
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
                                             'picture': 'pic',
                                             'price': ''
                                             })
        self.assertSuccessResponse(respEditItem)  

##############################################################################################################


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








