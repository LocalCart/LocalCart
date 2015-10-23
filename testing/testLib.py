"""
A library for functional testing of the backend API
"""

import unittest
import traceback
import httplib
import sys
import os
import json


class RestTestCase(unittest.TestCase):
    """
    Superclass for functional tests. Defines the boilerplate for the tests
    """

    # Lookup the name of the server to test
    serverToTest = "localhost:5000"
    if "TEST_SERVER" in os.environ:
        serverToTest = os.environ["TEST_SERVER"]
        # Drop the http:// prefix
        splits = serverToTest.split("://")
        if len(splits) == 2:
            serverToTest = splits[1]

    def makeRequest(self, url, method="GET", data={ }):
        """
        Make a request to the server.
        @param url is the relative url (no hostname)
        @param method is either "GET" or "POST"
        @param data is an optional dictionary of data to be send using JSON
        @result is a dictionary of key-value pairs
        """

        printHeaders = (os.getenv("VERBOSE") == '1')
        headers = { }
        body = ""
        if data is not None:
            headers = { "content-type": "application/json", "Accept": "application/json" }
            body = json.dumps(data)

        try:
            self.conn.request(method, url, body, headers)
        except Exception, e:
            if str(e).find("Connection refused") >= 0:
                print "Cannot connect to the server "+RestTestCase.serverToTest+". You should start the server first, or pass the proper TEST_SERVER environment variable"
                sys.exit(1)
            raise

        self.conn.sock.settimeout(100.0) # Give time to the remote server to start and respond
        resp = self.conn.getresponse()
        data_string = "<unknown"
        try:
            if printHeaders:
                print "\n****"
                print "  Request: "+method+" url="+url+" data="+str(data)
                print "  Request headers: "+str(headers)
                print ""
                print "  Response status: "+str(resp.status)
                print "  Response headers: "
                for h, hv in resp.getheaders():
                    print "    "+h+"  =  "+hv

            self.assertEquals(200, resp.status)
            data_string = resp.read()
            if printHeaders:
                print "  Response data: "+data_string
            # The response must be a JSON request
            # Note: Python (at least) nicely tacks UTF8 information on this,
            #   we need to tease apart the two pieces.
            self.assertTrue(resp.getheader('content-type') is not None, "content-type header must be present in the response")
            self.assertTrue(resp.getheader('content-type').find('application/json') == 0, "content-type header must be application/json")


            data = json.loads(data_string)
            return data

        except:
            # In case of errors dump the whole response,to simplify debugging
            print "Got exception when processing response to url="+url+" method="+method+" data="+str(data)
            print "  Response status = "+str(resp.status)
            print "  Response headers: "
            for h, hv in resp.getheaders():
                print "    "+h+"  =  "+hv
            print "  Data string: "+data_string
            print "  Exception: "+traceback.format_exc ()
            if not printHeaders:
                print "  If you want to see the request headers, use VERBOSE=1"
            raise


    def setUp(self):
        self.conn = httplib.HTTPConnection(RestTestCase.serverToTest, timeout=1)

    def tearDown(self):
        self.conn.close ()


## NOW SOME METHODS THAT ARE USEFUL FOR TESTING SMILES

class SmileTestCase(RestTestCase):
    """
    A base class for testing Smiles
    """

    def setUp(self):
        # Run first the setUp from the superclass
        RestTestCase.setUp(self)
        # As part of the setup, we grab the SMILE_SPACE from the environment
        assert 'SMILE_SPACE' in os.environ, "While running these tests you must specify SMILE_TEST=..."
        self.smileSpace = os.environ["SMILE_SPACE"]
        # We empty the smile space, before we start the test
        self.emptySmileSpace()

    def getSmiles(self,
                  count=None,
                  order_by=None):
        """
        Helper function to get some smiles
        """
        url = '/api/smiles?space='+self.smileSpace
        if count is not None:
            url += '&count='+str(count)
        if order_by is not None:
            url += '&order_by='+order_by

        respData = self.makeRequest(url, method='GET')
        return respData

    def emptySmileSpace(self):
        """
        Helper function to delete a smile space
        """
        url = '/api/smiles?space='+self.smileSpace
        self.makeRequest(url, method='DELETE')

    def assertSuccessResponse(self,
                              respData,
                              msg=None):
        """
        Check that the response is not an error response
        """
        self.assertEquals(1, respData['status'], msg)
