__copyright__ = "2015 Cisco Systems, Inc."

import configparser

# read config
config = configparser.ConfigParser()
config.read("config.ini")

mse_ip = config.get('mse', 'mse_ip')
mse_api_base = config.get('mse', 'mse_api_base')

clients_api = config.get('mse', 'clients_api')
map_api = config.get('mse', 'map_api')

mse_username = config.get('mse', 'username')
mse_password = config.get('mse', 'password')
local_host_ip = config.get('local', 'local_host_ip')

default_map = config.get('resource', 'default_map')

# build mse api
# it follow the api of MSE 8.0
https_label = "https://"

get_all_clients_api = '%s%s%s%s' % (https_label, mse_ip, mse_api_base, clients_api)
get_map_api = '%s%s%s%s' % (https_label, mse_ip, mse_api_base, map_api)