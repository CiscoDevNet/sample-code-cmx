__author__ = "Ronak Lakhwani"
__copyright__ = "2015 Cisco Systems, Inc."

# General Imports
from datetime import datetime
import random

# configuration
import configparser

# Imports for calling the CMX Rest API
from urllib.request import *
from urllib.error import URLError

# Imports for reading the xml response
from bs4 import BeautifulSoup

# Imports for reading the json response
import json


# Imports for plotting the graph
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import Layout, Marker, Scatter, XAxis, YAxis, Data, Figure

# Imports for certificate fail error
# The below two lines should be uncommented if you are getting [SSL: CERTIFICATE_VERIFY_FAILED] Error. This depends on the browser
# and on the environment depending on whether you have the certificate installed or not.
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Read config Starts
config = configparser.ConfigParser()
config.read("config.ini")
mse_ip = config.get('mse', 'mse_ip')
username = config.get('mse', 'username')
password = config.get('mse', 'password')
url_suffix = config.get('mse', 'url_suffix')
macs = config.get('local', 'macs').split(",")
response_format = config.get('local', 'response_format')
plotly_username = config.get('plotly', 'plotly_username')
plotly_api_key = config.get('plotly', 'plotly_api_key')
interval = int(config.get('local', 'interval'))
# Read config Ends

# Constant
url_prefix = "https://"
url_query_parameters1 = "?/page=0"
url_query_parameters2 = "&pageSize="


'''
Below method is used to return the response from the CMX API
whose end point is in the URL variable.
Username and Password are used to access the CMX API.
'''
def get_response(URL, username, password, response_format):
    '''
     Returns the response in the form of dict where keys are isError and others.
     if isError is True then dict contains the other keys such as data which contains the description of the message
     if isError is False then dict contains the other keys such as width,length,data.
    '''
    response_dict = {}
    for mac in macs:
        try:
            mac_dict = {}
            conn = HTTPPasswordMgrWithDefaultRealm()
            nURL = URL + mac + url_query_parameters1 + url_query_parameters2 + str(interval)
            print(nURL)
            conn.add_password(None, nURL, username, password)
            handler = HTTPBasicAuthHandler(conn)
            opener = build_opener(handler)
            opener.addheaders = [('Accept', 'application/' + response_format)]
            install_opener(opener)
            page = urlopen(nURL).read()
            if len(page):
                page = page.decode('utf-8')
                if response_format == "xml" :
                    mac_dict = get_useful_data_from_XML(page)
                elif response_format == "json":
                    mac_dict = get_useful_data_from_json(page)
                if response_dict.get("data") is None:
                    response_dict = mac_dict
                else:
                    response_dict.get("data").update(mac_dict["data"])
        except URLError as e:
            print("Error while calling history api for client : " + mac)
            print("Error message = " + e.msg)
    
    if response_dict.get("data") is None:
        response_dict['data'] = "URL is malformed"
        response_dict['isError'] = True
        return response_dict
    else:
        response_dict['isError'] = False
        return response_dict

'''
Gets the date in the string format 2015-03-17T00:27:33.437+0000 and converts it into 2015-03-17 00:27:33 and then returns the date_object
'''
def parse_date(string_date):
    string_date = string_date[0:10] + " " + string_date[11:19]
    date_object = datetime.strptime(string_date, "%Y-%m-%d %H:%M:%S")
    return date_object

'''
Extracts the useful data from the json response(in case response format in config is json) and returns the dict.
'''
def get_useful_data_from_json(json_response):
    '''
    Parses the json_response and returns the dict with keys as width, length and the data
    1. width contains the value of the width
    2. length contains the value of the length
    3. data contains the list of tuples where tuples are in the format (lastlocatedtime,x,y)
    All the above three are returned only when you get location from the json_response otherwise an empty dict is returned
    '''
    data = {}
    json_dict = json.loads(json_response)
    if len(json_dict['Locations']['entries']) > 0:
        width = json_dict['Locations']['entries'][0]['MapInfo']['Dimension']['width']
        length = json_dict['Locations']['entries'][0]['MapInfo']['Dimension']['length']

        for wirelessclientlocation in json_dict['Locations']['entries']:
            mac = wirelessclientlocation["macAddress"]
            if mac in macs:
                x = wirelessclientlocation["MapCoordinate"]["x"]
                y = wirelessclientlocation["MapCoordinate"]["y"]
                lastlocatedtime = parse_date(wirelessclientlocation["Statistics"]["lastLocatedTime"])
                data.setdefault(mac, []).append((lastlocatedtime, x, y))
        return {"width" : width, "length":length, "data":data}
    else :
        return {}

'''
Extracts the useful data from the json response(in case response format in config is xml) and returns the dict.
'''
def get_useful_data_from_XML(xml):
    '''
    Parses the xml and returns the dict with keys as width, length and the data
    1. width contains the value of the width
    2. length contains the value of the length
    3. data is in the form of dictionaries containing key as macaddress(provided above in congiguration section)
    and the corresponding values as list of tuples where tuples are in the format (lastlocatedtime,x,y)
    All the above three are returned only when you get location from the jsonResponse otherwise an empty dict is returned
    '''
    data = {}
    xml_format = BeautifulSoup(xml)
    wirelessclientlocations = xml_format.find_all("wirelessclientlocation")
    if len(wirelessclientlocations) > 0:
        width = xml_format.locations.wirelessclientlocation.mapinfo.dimension['width']
        length = xml_format.locations.wirelessclientlocation.mapinfo.dimension['length']
        for wirelessclientlocation in wirelessclientlocations:
            mac = wirelessclientlocation["macaddress"]
            if mac in macs:
                x = wirelessclientlocation.mapcoordinate['x']
                y = wirelessclientlocation.mapcoordinate['y']
                lastlocatedtime = parse_date(wirelessclientlocation.statistics['lastlocatedtime'])
                data.setdefault(mac, []).append((lastlocatedtime, x, y))
        return {"width" : width, "length":length, "data":data}
    else:
        return {}

'''
Method which reads the dict and renders the response on to the Plotly framework.
'''
def plot_data(data_dict):
    '''
    Plots the data on the Plotly Framework.
    '''
    py.sign_in(plotly_username, plotly_api_key)
    tls.set_credentials_file(username=plotly_username,
                                 api_key=plotly_api_key)
    layout = Layout(
                showlegend=True,
                autosize=True,
                height=800,
                width=800,
                title="MAP",
                xaxis=XAxis(
                    zerolinewidth=4,
                    gridwidth=1,
                    showgrid=True,
                    zerolinecolor="#969696",
                    gridcolor="#bdbdbd",
                    linecolor="#636363",
                    mirror=True,
                    zeroline=False,
                    showline=True,
                    linewidth=6,
                    type="linear",
                    range=[0, data_dict["length"]],
                    autorange=False,
                    autotick=False,
                    dtick=15,
                    tickangle=-45,
                    title="X co-ordinate"
                    ),
                yaxis=YAxis(
                    zerolinewidth=4,
                    gridwidth=1,
                    showgrid=True,
                    zerolinecolor="#969696",
                    gridcolor="#bdbdbd",
                    linecolor="#636363",
                    mirror=True,
                    zeroline=False,
                    showline=True,
                    linewidth=6,
                    type="linear",
                    range=[data_dict["width"], 0],
                    autorange=False,
                    autotick=False,
                    dtick=15,
                    tickangle=-45,
                    title="Y co-ordinate"
                    )
                )
    mac_history_data = data_dict['data']
    processed_data = []
    for mac, p_data in mac_history_data.items():
        if len(p_data):
            p_data = sorted(p_data, key=lambda x:x[0])
            color = color_generator()
            plot_data = Scatter(
                x=[x[1] for x in p_data],
                y=[y[2] for y in p_data],
                mode='lines + text',
                text=list(range(1, len(p_data) + 1)),
                name=mac,
                marker=Marker(color=color),
                opacity="0.6",
                legendgroup = mac,
            )
            processed_data.append(plot_data)
            
            startData = Scatter(
            x=[p_data[0][1]],
            y=[p_data[0][2]],
            mode='markers',
            marker=Marker(color=color, size="10", symbol = "triangle-left"),
            showlegend=False,
            text=["Start point " + mac],
            legendgroup=mac,
            )
            processed_data.append(startData)
            
            endData = Scatter(
            x=[p_data[-1][1]],
            y=[p_data[-1][2]],
            mode='markers',
            marker=Marker(color=color, size="10"),
            showlegend=False,
            text=["End point " + mac],
            legendgroup=mac,
            )
            processed_data.append(endData)
    data = Data(processed_data)
    fig = Figure(data=data, layout=layout)
    py.plot(fig, filename='Sample Code For History Of Clients ')

'''
Returns the random color in the form of hexadecimal numbers in the format #XXXXXX
'''
def color_generator():
    def r():
        '''
        Returns the random hexadecimal number between 0-255 in the form of XX
        '''
        hex_random = hex(random.randint(0, 255))[2:]
        return hex_random if len(hex_random) >= 2 else hex_random + "0"
    return "#" + r() + r() + r()

'''
Main Method to Invoke the Application
'''
if __name__ == '__main__':
    URL = url_prefix + mse_ip + url_suffix
    print("Graph plot showing the motion of the client will automatically appear in the browser after program is run successfully.")
    data_dict = get_response(URL, username, password, response_format)
    if data_dict['isError'] == False:
        if len(data_dict['data']) > 0:
            plot_data(data_dict)
        else:
            print('No clients found')
    else:
        print("Error = ", data_dict['data'])