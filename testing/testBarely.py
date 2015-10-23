"""
This file contains a small subset of the tests we will run on your backend submission
"""

import unittest
import os
import testLib

class TestSmiles(testLib.SmileTestCase):

    ###
    ### THESE ARE THE ACTUAL TESTS
    ###
    def testAdd1(self):
        """
        Test adding one smile
        """
        respCreate = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'A shy smile',
                                             'space' : self.smileSpace,
                                             'story' : 'Once upon a time I was a shy boy...',
                                             'happiness_level' : 1
                                             })
        self.assertSuccessResponse(respCreate)
        self.assertEquals(0, respCreate['smile']['like_count'])
        self.assertEquals('A shy smile', respCreate['smile']['title'])

        # Now read the smiles
        respGet = self.getSmiles(count='all')
        self.assertSuccessResponse(respGet)
        self.assertEquals(1, len(respGet['smiles']))
        self.assertEquals(respCreate['smile']['id'], respGet['smiles'][0]['id'])
    

    def testGetPost(self):
        """
        Test checking the the GET request
        """
        respCreate = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'A different smile',
                                             'space' : self.smileSpace,
                                             'story' : 'All of this filler text should match',
                                             'happiness_level' : 3
                                             })
        self.assertSuccessResponse(respCreate)
        self.assertEquals(0, respCreate['smile']['like_count'])
        self.assertEquals('A different smile', respCreate['smile']['title'])
        self.assertEquals(self.smileSpace, respCreate['smile']['space'])
        self.assertEquals('All of this filler text should match', respCreate['smile']['story'])
        self.assertEquals(3, respCreate['smile']['happiness_level'])

        respCreate2 = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'Another different smile',
                                             'space' : self.smileSpace,
                                             'story' : 'All of this filler text should match again',
                                             'happiness_level' : 2
                                             })
        self.assertSuccessResponse(respCreate2)
        self.assertEquals(0, respCreate2['smile']['like_count'])
        self.assertEquals('Another different smile', respCreate2['smile']['title'])

        respGet = self.makeRequest("/api/smiles?space=" + self.smileSpace + "&count=2&order_by=created_at", method="GET")
        self.assertSuccessResponse(respGet)
        self.assertEquals(2, len(respGet['smiles']))
        self.assertEquals(respCreate['smile']['id'], respGet['smiles'][1]['id'])
        self.assertEquals(respCreate2['smile']['id'], respGet['smiles'][0]['id'])

        for i in range(0, 18):
            self.makeRequest("/api/smiles", method="POST",
                                        data = { 'title' : 'Another different smile ' + str(i),
                                                 'space' : self.smileSpace,
                                                 'story' : 'All of this filler text should match again',
                                                 'happiness_level' : 2
                                                 })
        respGet2 = self.getSmiles(count=None, order_by='created_at')
        self.assertSuccessResponse(respGet2)
        self.assertEquals(20, len(respGet2['smiles']))
        self.assertEquals(respCreate['smile']['id'], respGet2['smiles'][19]['id'])
        self.assertEquals(respCreate['smile']['title'], respGet2['smiles'][19]['title'])
        self.assertEquals(respCreate2['smile']['id'], respGet2['smiles'][18]['id'])


    def testLike(self):
        """
        Testing the like functionality
        """
        respCreate = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'A different smile',
                                             'space' : self.smileSpace,
                                             'story' : 'All of this filler text should match',
                                             'happiness_level' : 3
                                             })
        self.assertSuccessResponse(respCreate)
        self.assertEquals(0, respCreate['smile']['like_count'])
        self.assertEquals('A different smile', respCreate['smile']['title'])
        start = respCreate['smile']['updated_at']
        id1 = respCreate['smile']['id']
        respCreate2 = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'Another different smile',
                                             'space' : self.smileSpace,
                                             'story' : 'All of this filler text should match again',
                                             'happiness_level' : 2
                                             })
        start2 = respCreate2['smile']['updated_at']
        id2 = respCreate2['smile']['id']
        self.assertSuccessResponse(respCreate2)
        self.assertEquals(0, respCreate2['smile']['like_count'])
        respLike = self.makeRequest("/api/smiles/" + str(id2) + "/like", method="POST", data = {})
        respGet = self.getSmiles(count=None, order_by='created_at')
        s1 = respGet['smiles'][1]
        s2 = respGet['smiles'][0]
        liketime = s1['updated_at']
        liketime2 = s2['updated_at']
        self.assertTrue(start == liketime)
        self.assertTrue(start2 < liketime2)
        self.assertEquals(0, s1['like_count'])
        self.assertEquals(1, s2['like_count'])
        respLike = self.makeRequest("/api/smiles/" + str(id2) + "/like", method="POST", data = {})
        respLike = self.makeRequest("/api/smiles/" + str(id2) + "/like", method="POST", data = {})
        respLike = self.makeRequest("/api/smiles/" + str(id1) + "/like", method="POST", data = {})
        respGet = self.getSmiles(count=None, order_by='created_at')
        s1 = respGet['smiles'][1]
        s2 = respGet['smiles'][0]
        self.assertEquals(1, s1['like_count'])
        self.assertEquals(3, s2['like_count'])
        respLike = self.makeRequest("/api/smiles/asdfa3/like", method="POST", data = {})
        self.assertEquals(-1, respLike['status'])
        self.assertEquals("Invalid smile id", respLike['errors'][0])
        respLike = self.makeRequest("/api/smiles/0/like", method="POST", data = {})
        self.assertEquals(-1, respLike['status'])
        self.assertEquals("Invalid smile id", respLike['errors'][0])
        respLike = self.makeRequest("/api/smiles/-1/like", method="POST", data = {})
        self.assertEquals(-1, respLike['status'])
        self.assertEquals("Invalid smile id", respLike['errors'][0])



    def testDelete(self):
        """
        Testing the like functionality
        """
        respCreate = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'A different smile',
                                             'space' : self.smileSpace,
                                             'story' : 'All of this filler text should match',
                                             'happiness_level' : 3
                                             })
        self.assertSuccessResponse(respCreate)
        self.assertEquals(0, respCreate['smile']['like_count'])
        self.assertEquals('A different smile', respCreate['smile']['title'])
        self.emptySmileSpace()
        respGet = self.getSmiles()
        self.assertSuccessResponse(respGet)
        self.assertEquals(0, len(respGet['smiles']))
        respDel = self.makeRequest('/api/smiles?space=', method='DELETE', data={})
        self.assertEquals(-1, respDel['status'])
        self.assertEquals("space must be non-empty", respDel['errors'][0])



    def testGetErrors(self):
        resp = self.makeRequest("/api/smiles?space=&count=2&order_by=created_at", method="GET")
        self.assertEquals(-1, resp['status'])
        self.assertEquals("space must be non-empty", resp['errors'][0])
        resp = self.makeRequest("/api/smiles?space=" + self.smileSpace + "&count=0&order_by=created_at", method="GET")
        self.assertEquals(-1, resp['status'])
        self.assertEquals("Invalid count", resp['errors'][0])
        resp = self.makeRequest("/api/smiles?space=" + self.smileSpace + "&count=2&order_by=asdfasdfasdf", method="GET")
        self.assertEquals(-1, resp['status'])
        self.assertEquals("Invalid order_by", resp['errors'][0])



    def testPostErrors(self):
        resp = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'A different smile',
                                             'space' : '',
                                             'story' : 'All of this filler text should match',
                                             'happiness_level' : 3
                                             })
        self.assertEquals(-1, resp['status'])
        self.assertEquals("space must be non-empty", resp['errors'][0])
        resp = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'A different smile',
                                             'space' : 'FILLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL' + \
                                                       'LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL' + \
                                                       'LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL' + \
                                                       'LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL' + \
                                                       'LLLLLLLLLLLLLLLLLER',
                                             'story' : 'All of this filler text should match',
                                             'happiness_level' : 3
                                             })
        self.assertEquals(-1, resp['status'])
        self.assertEquals("space must be at most 128 characters", resp['errors'][0])
        resp = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : '',
                                             'space' : self.smileSpace,
                                             'story' : 'All of this filler text should match',
                                             'happiness_level' : 3
                                             })
        self.assertEquals(-1, resp['status'])
        self.assertEquals("title must be non-empty", resp['errors'][0])
        resp = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'FILLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL' + \
                                                       'LLLLLLLLLLLLLLLLLLLLLLLLLLER',
                                             'space' : self.smileSpace,
                                             'story' : 'All of this filler text should match',
                                             'happiness_level' : 3
                                             })
        self.assertEquals(-1, resp['status'])
        self.assertEquals("title must be at most 64 characters", resp['errors'][0])
        resp = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'A different smile',
                                             'space' : self.smileSpace,
                                             'story' : '',
                                             'happiness_level' : 3
                                             })
        self.assertEquals(-1, resp['status'])
        self.assertEquals("story must be non-empty", resp['errors'][0])
        resp = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'A different smile',
                                             'space' : self.smileSpace,
                                             'story' : 'All of this filler text should match',
                                             'happiness_level' : -1
                                             })
        self.assertEquals(-1, resp['status'])
        self.assertEquals("happiness_level must be an integer from 1 to 3", resp['errors'][0])
        resp = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'A different smile',
                                             'space' : self.smileSpace,
                                             'story' : 'All of this filler text should match',
                                             'happiness_level' : 0
                                             })
        self.assertEquals(-1, resp['status'])
        self.assertEquals("happiness_level must be an integer from 1 to 3", resp['errors'][0])
        resp = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'A different smile',
                                             'space' : self.smileSpace,
                                             'story' : 'All of this filler text should match',
                                             'happiness_level' : 4
                                             })
        self.assertEquals(-1, resp['status'])
        self.assertEquals("happiness_level must be an integer from 1 to 3", resp['errors'][0])
        resp = self.makeRequest("/api/smiles", method="POST",
                                    data = { 'title' : 'A different smile',
                                             'space' : self.smileSpace,
                                             'story' : 'All of this filler text should match',
                                             'happiness_level' : 'a'
                                             })
        self.assertEquals(-1, resp['status'])
        self.assertEquals("happiness_level must be an integer from 1 to 3", resp['errors'][0])





        