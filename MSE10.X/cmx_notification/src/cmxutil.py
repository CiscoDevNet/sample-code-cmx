__author__ = "Yaojing Liu"
__copyright__ = "2015 Cisco Systems, Inc."


# public library
from urllib import parse
from urllib.request import *
from urllib.error import URLError
from http.client import HTTPSConnection
from base64 import b64encode
import json
import os
import sys
import ssl


def get_json_response(server, api, username, password):
        """
        Returns the response from the URL specified
        """
        try:
            # lib opener
            response = {}
            context = ssl._create_unverified_context()
            conn = HTTPSConnection(server, context=context)
            auth = str.encode("%s:%s" % (username, password))
            user_and_pass = b64encode(auth).decode("ascii")
            headers = {'Authorization': 'Basic %s' % user_and_pass, "Accept": 'application/json'}
            conn.request('GET', api, headers=headers)
            res = conn.getresponse()
            bit_data = res.read()
            string_data = bit_data.decode(encoding='UTF-8')
            response['data'] = string_data
            response['status'] = 200
        except:
            print("--Unexpected error:", sys.exc_info()[1])
            response['data'] = sys.exc_info()[1]
            response['status'] = 400

        return response

