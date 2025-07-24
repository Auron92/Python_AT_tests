import pytest_check as check
from loguru import logger
import pytest
from configs.TCP_client_LabVIEW_Python_connection_DSP_AT import data_transfer_with_VI
from configs.configurations import labview_connection
from configs.TCP_client_LabVIEW_Python_connection_DSP_AT import HF_Test
from configs.configurations import device_info


def test_authentication(LX_connection):
   if LX_connection == 'FAILED':
      pytest.exit("AUTHENTICATION_FAILED")
   else:
      logger.info("AUTH DONE!")
      assert "Auth complete!"


class Test_DSP_AT:
      
   def test_AT_task1(self, LX_connection): 
      result = LX_connection.run_test_ssh_1()
      answer = data_transfer_with_VI(labview_connection, device_info, test_name=HF_Test.Singletone)
      # ПРОВЕРКА ОТВЕТА ОТ LW без подключенного АСРВ
      check.equal(answer, "ERR_-1", "Something doesnt work right")
      check.equal(result, "Hello, World!\n", "test_AT_task1 failed")
      

   def test_AT_task2(self, LX_connection):
      result = LX_connection.run_test_ssh_2()
      answer = data_transfer_with_VI(labview_connection, device_info, test_name=HF_Test.Loopback)
      # ПРОВЕРКА ОТВЕТА ОТ LW без подключенного АСРВ
      check.equal(answer, "ERR_-1", "Something doesnt work right")
      check.equal(result, "snap\n", "test_AT_task2 failed")




# для одиночных запусков

   # def test_AT_task1(self, LX_connection): 
   #    if check.not_equal(LX_connection, 'FAILED', "AUTHENTICATION_FAILED!"):
   #       result = LX_connection.run_tests_LX()
   #       check.equal(result, "Hello, World!\n", "TEST1 не прошел")

   # def test_AT_task2(self, LX_connection):
   #    if check.not_equal(LX_connection, 'FAILED', "AUTHENTICATION_FAILED!"):
   #       result = LX_connection.run_testToneFreq()
   #       check.equal(result, "snap\n", "TEST2 не прошел")

   # check