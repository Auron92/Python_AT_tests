import yaml
from os import path

ini_path = path.dirname(path.abspath(__file__))
ini_path = path.join(ini_path, 'config.yaml')

# Reading a INI file
# config = configparser.ConfigParser()
# config.read(ini_path)
# USERNAME = config.get('DEFAULT','USERNAME')
# PASSWORD = config.get('DEFAULT','PASSWORD')


# Reading a YAML file
with open(ini_path, "r") as file:
    config = yaml.safe_load(file)

HOST = config["server"]["host"]
PORT = config["server"]["port"]
USERNAME = config["user"]["username"]
PASSWORD = config["user"]["password"]

server_auth = {
    'hostname': HOST,
    'username': USERNAME,
    'password': PASSWORD,
    'port': PORT,
}

LABVIEW_HOST = config["Labview_client"]["host"]
LABVIEW_PORT = config["Labview_client"]["port"]

labview_connection = (LABVIEW_HOST, LABVIEW_PORT)

DEVICE_NAME = config["device"]['name']
DEVICE_SN = config["device"]['sn']

device_info = f"{DEVICE_NAME}-{DEVICE_SN}"
#
