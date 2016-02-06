__author__ = "Yaojing Liu"
__copyright__ = "2015 Cisco Systems, Inc."


# public library
from urllib import parse
from urllib.request import *
from urllib.error import URLError

import os


# function to get json response
def get_json_response(_url, username, password):
    """
    Returns the response from the URL specified
    """
    try:
        # lib opener
        response = {}
        conn = HTTPPasswordMgrWithDefaultRealm()
        conn.add_password(None, _url, username, password)
        handler = HTTPBasicAuthHandler(conn)
        opener = build_opener(handler)

        # set header to get json
        opener.addheaders = [('Accept', 'application/json')]
        install_opener(opener)
        result = urlopen(_url).read()
        response['data'] = result
        response['status'] = 200
    except URLError as e:
        response['data'] = e
        response['status'] = e.code
        print(e)

    return response


# function to get image response
def get_image_response(_url, username, password):
    """
     Returns the response from the URL specified
    """
    try:
        # lib opener
        _url = parse.quote(_url, ':/')
        # print 'url', _url
        conn = HTTPPasswordMgrWithDefaultRealm()
        conn.add_password(None, _url, username, password)
        handler = HTTPBasicAuthHandler(conn)
        opener = build_opener(handler)

        # set header to get json
        install_opener(opener)
        result = urlopen(_url).read()

        if os.path.exists("images") is False:
            os.mkdir("images")

        output = open("images/temp.jpeg", "wb")
        output.write(result)
        output.close()
    except URLError as e:
        print(e)
    except IOError as e:
        print(e)
    return "images/temp.jpeg"
