import socket
import enum

class HF_Test(enum.IntEnum):
    Singletone = 0
    Phaseshift = 1
    Freqresp = 2
    Loopback = 3
    

def data_transfer_with_VI(ip_addr:tuple, device_info:str, test_name:HF_Test) -> str:
    """
    This function provides: 1. TCP/IP-connection to LabVIEW VI executing program;
    2. send message, which includes device_info, test_name;
    3. receive a message from LabVIEW about result of test execution - ok/fail.

    Arguments:\n
    ip_addr - tuple of ip adress & port number (example - ("10.77.46.144", 8880))\n
    device_info - information about testing device (serial number, firmware, etc.)\n
    test_name - attribute of class Test (default - "Test.testToneFreq")
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: #Context Manager
        sock.connect(ip_addr) # attempt to connect to LABVIEW VI
        message = f"Test_type = {test_name}\nDevice_name = {device_info}".encode() # converts the data needed to send to LabVIEW in byte string
        sock.send(message) # send a message to LabVIEW VI
        is_test_passed = sock.recv(20) # receive an answer from LabVIEW VI
        
        
    return is_test_passed.decode() # test result (fail/ok) is output of function
        




