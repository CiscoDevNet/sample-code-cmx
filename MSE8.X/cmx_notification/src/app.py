__author__ = "Yaojing Liu"
__copyright__ = "2015 Cisco Systems, Inc."

# !flask/bin/python
# run with flask
from flask import Flask, jsonify, request, Response, make_response, abort, send_file, json

# configuration

import json
# customer library
from cmxutil import get_json_response, get_image_response
from crosutil import crossdomain
from areacontainer import areas_container, area_none
from configreader import *


# create simple flask server
app = Flask(__name__)


# default handler
@app.errorhandler(404)
@crossdomain(origin='*')
def not_found(error):
    response = jsonify({'error': 'Not found'})
    return response

@app.errorhandler(400)
def not_found(error):
    response = jsonify({'error': error.description})
    return response

# get all clients from cmx
@app.route('/', methods=['GET'])
@crossdomain(origin='*')
def get_default():
    return Response("Hello Developer, please visit following page and follow Usage section to use this sample code:\n"
                    "https://github.com/CiscoDevNet/sample-code-cmx/MSE8.0/cmx_notification")

# get default map images
@app.route('/cmx/api/v1.0/map', methods=['GET'])
@crossdomain(origin='*')
def get_default_image():
    map_id = request.args.get('map')
    if map_id:
        default_map_url = get_map_api + map_id
    else:
        default_map_url = get_map_api + default_map
    filename = get_mse_image(default_map_url)
    # return send_file(img, as_attachment=True, attachment_filename='map.jpg')
    return send_file(filename, mimetype='image/jpg')


# get all clients from cmx
@app.route('/cmx/api/v1.0/clients', methods=['GET'])
@crossdomain(origin='*')
def get_clients():
    data = get_mse_response(get_all_clients_api)['data']
    response = Response(response=data,
                        status=200,
                        mimetype="application/json")
    return response


# get client with certain mac from cmx
@app.route('/cmx/api/v1.0/clients/<string:mac>', methods=['GET'])
@crossdomain(origin='*')
def get_client_mac(mac):
    mac_url = get_all_clients_api + "/" + mac
    data = get_mse_response(mac_url)['data']
    response = Response(response=data,
                        status=200,
                        mimetype="application/json")
    return response


# get all areas info
@app.route('/cmx/api/v1.0/areas', methods=['GET'])
@crossdomain(origin='*')
def get_areas():
    data = jsonify({'areas': areas_container})
    return data


# get area info of certain area_id
@app.route('/cmx/api/v1.0/areas/<string:area_id>', methods=['GET'])
@crossdomain(origin='*')
def get_area(area_id):
    for area in areas_container:
        print(area['areaId'])
        if area['areaId'] == area_id:
            return jsonify(area)

    return jsonify(area_none)


# create new area
@app.route('/cmx/api/v1.0/areas', methods=['POST'])
@crossdomain(origin='*')
def create_area():
    if request.json is None or 'areaId' not in request.json:
        abort(400)
    areas_container.append(request.json)
    return jsonify(request.json), 201


# check current area of certain mac, return the current area if inside or none if outside
@app.route('/cmx/api/v1.0/areas/mac/<string:mac>', methods=['GET'])
@crossdomain(origin='*')
def get_area_of_mac(mac):
    if mac:
        mac_url = get_all_clients_api + "/" + mac
        response = get_mse_response(mac_url)
        if response['status'] is 200:
            data = response['data']
            data_string = data.decode()
            data_json = json.loads(data_string)
            if data_json:
                location = data_json['WirelessClientLocation']
                coordinates = location['MapCoordinate']
                x = float(coordinates['x'])
                y = float(coordinates['y'])

                if x and y:
                    print('location of', mac, x, y)
                    for area in areas_container:
                        if check_pos_in_area(x, y, area):
                            return jsonify(area)

    return jsonify(area_none)

# check current area of certain mac, return the current area if inside or none if outside
@app.route('/cmx/api/v1.0/clients/area/<string:area_id>', methods=['GET'])
@crossdomain(origin='*')
def get_macs_in_area(area_id):
    clients = []
    if area_id:
        for area in areas_container:
            if area['areaId'] == area_id:
                response = get_mse_response(get_all_clients_api)
                if response['status'] is 200:
                    data = response['data']
                    data_string = data.decode()
                    data_json = json.loads(data_string)
                    entries = data_json['Locations']['entries']
                    for entry in entries:
                        coordinates = entry['MapCoordinate']
                        x = float(coordinates['x'])
                        y = float(coordinates['y'])
                        if x and y:
                            if check_pos_in_area(x, y, area):
                                clients.append(entry)
    result = dict()
    result["clients"] = clients
    return jsonify(result)


def get_mse_response(api):
    return get_json_response(api, mse_username, mse_password)


def get_mse_image(api):
    return get_image_response(api, mse_username, mse_password)


def check_pos_in_area(x, y, area):
    dimension = area['dimension']
    offset_x = float(dimension['offsetX'])
    offset_y = float(dimension['offsetY'])
    length = float(dimension['length'])
    width = float(dimension['width'])
    if (offset_x <= x <= (offset_x + width)) and (offset_y <= y <= (offset_y + length)):
        return True
    return False

if __name__ == '__main__':
    app.run(host=local_host_ip, debug=False)