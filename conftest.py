import pytest
import paramiko
import logging
from configs.configurations import server_auth
from configs.connections import LX



@pytest.fixture(scope="session")  
def LX_connection():
    try:
        lx = LX()
        lx.create_ssh_connection()
        yield lx
        lx.close_ssh_connection()
    except paramiko.AuthenticationException as e:
        yield "FAILED"


def pytest_configure(config):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')