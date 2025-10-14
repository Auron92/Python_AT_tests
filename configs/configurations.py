import yaml
from os import path
import configparser
import os

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
    'port': PORT,
}

LABVIEW_HOST = config.get("Labview_client","host")
LABVIEW_PORT = config.get("Labview_client","port")

labview_connection = (LABVIEW_HOST, int(LABVIEW_PORT))

DEVICE_NAME = config.get("device","name")
DEVICE_SN = config.get("device","sn")

device_info = f"{DEVICE_NAME}-{DEVICE_SN}"
#

ALLURE_CTL_PATH = config.get("Allure","exe_path")
ENDPOINT = config.get("Allure","endpoint")
TOKEN = config.get("Allure","token")
PROJECT_ID = config.get("Allure","project_id")
LAUNCH_NAME = config.get("Allure","launch_name")

allure_upload = {
    'allurectl_path': ALLURE_CTL_PATH,
    'endpoint': ENDPOINT,
    'token':TOKEN,
    'project_id': PROJECT_ID,
    'launch_name': LAUNCH_NAME,
}
