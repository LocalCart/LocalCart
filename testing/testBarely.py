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




        
    #     # Now read the smiles
    #     respGet = self.getSmiles(count='all')
    #     self.assertSuccessResponse(respGet)
    #     self.assertEquals(1, len(respGet['smiles']))
    #     self.assertEquals(respCreate['smile']['id'], respGet['smiles'][0]['id'])

    # def testAdd3(self):
    #     """
    #     Test adding three smile
    #     """
    #     respCreate1 = self.makeRequest("/api/smiles", method="POST",
    #                                 data = { 'title' : 'A shy smile1',
    #                                          'space' : self.smileSpace,
    #                                          'story' : 'Once upon a time I was a shy boy...',
    #                                          'happiness_level' : 1
    #                                          })
    #     respCreate2 = self.makeRequest("/api/smiles", method="POST",
    #                                 data = { 'title' : 'A shy smile2',
    #                                          'space' : self.smileSpace,
    #                                          'story' : 'Once upon a time I was a shy boy...',
    #                                          'happiness_level' : 2
    #                                          })
    #     respCreate3 = self.makeRequest("/api/smiles", method="POST",
    #                                 data = { 'title' : 'A shy smile3',
    #                                          'space' : self.smileSpace,
    #                                          'story' : 'Once upon a time I was a shy boy...',
    #                                          'happiness_level' : 3
    #                                          })
    #     self.assertSuccessResponse(respCreate1)
    #     self.assertEquals(0, respCreate1['smile']['like_count'])
    #     self.assertSuccessResponse(respCreate2)
    #     self.assertEquals(0, respCreate2['smile']['like_count'])
    #     self.assertSuccessResponse(respCreate3)
    #     self.assertEquals(0, respCreate3['smile']['like_count'])
    #     self.assertEquals('A shy smile1', respCreate1['smile']['title'])
    #     self.assertEquals('A shy smile2', respCreate2['smile']['title'])
    #     self.assertEquals('A shy smile3', respCreate3['smile']['title'])
    #     self.assertEquals(1, respCreate1['smile']['happiness_level'])
    #     self.assertEquals(2, respCreate2['smile']['happiness_level'])
    #     self.assertEquals(3, respCreate3['smile']['happiness_level'])

    #     respGet = self.getSmiles(count='all')
    #     self.assertSuccessResponse(respGet)
    #     self.assertEquals(3, len(respGet['smiles']))
    #     # self.assertEquals(respCreate['smile']['id'], respGet['smiles'][0]['id'])

    # # test for error when create new smile



    
    # def testIncrementLike(self):

    #     respCreate = self.makeRequest("/api/smiles", method="POST",
    #                                 data = { 'title' : 'A shy smile',
    #                                 'space' : self.smileSpace,
    #                                 'story' : 'Once upon a time I was a shy boy...',
    #                                 'happiness_level' : 1
    #                                 })
    #     respGet = self.getSmiles(count='all')
    #     self.assertSuccessResponse(respGet)
    #     resp_id = respGet['smiles'][0]['id']
    #     url = "/api/smiles/" + str(resp_id) + "/like/"
    #     respInc = self.makeRequest(url, method="POST")

    #     respGet = self.getSmiles(count='all')
    #     self.assertSuccessResponse(respGet)
    #     self.assertEquals(1, respGet['smiles'][0]['like_count'])







