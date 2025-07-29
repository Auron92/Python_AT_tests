import yaml
from os import path
import configparser

ini_path = path.dirname(path.abspath(__file__))
ini_path = path.join(ini_path, 'config.ini')

# Reading a INI file
config = configparser.ConfigParser()
config.read(ini_path)
# USERNAME = config.get('DEFAULT','USERNAME')
# PASSWORD = config.get('DEFAULT','PASSWORD')


# Reading a YAML file
#with open(ini_path, "r") as file:
#    config = yaml.safe_load(file)

HOST = config.get("server","host")
PORT = config.get("server","port")
USERNAME = config.get("user","username")
PASSWORD = config.get("user","password")

server_auth = {
    'hostname': HOST,
    'username': USERNAME,
    'password': PASSWORD,
    'port': int(PORT),
}

LABVIEW_HOST = config.get("Labview_client","host")
LABVIEW_PORT = config.get("Labview_client","port")

labview_connection = (LABVIEW_HOST, int(LABVIEW_PORT))

DEVICE_NAME = config.get("device","name")
DEVICE_SN = config.get("device","sn")

device_info = f"{DEVICE_NAME}-{DEVICE_SN}"
#
