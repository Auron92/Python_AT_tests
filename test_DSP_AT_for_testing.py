import pytest_check as check
import logging
import pytest
import allure
from configs.TCP_client_LabVIEW_Python_connection_DSP_AT import data_transfer_with_VI
from configs.configurations import labview_connection
from configs.TCP_client_LabVIEW_Python_connection_DSP_AT import HF_Test
from configs.configurations import device_info

#logger = logging.getLogger(__name__)


@allure.id("62335")
@allure.title("Аутентификация пользователя")
def test_authentication(LX_connection):
   if LX_connection == 'FAILED':
      pytest.exit("AUTHENTICATION_FAILED")
   else:
      logging.info("AUTH DONE!")
      assert "Auth complete!"

@allure.feature("DSP_AT")
class Test_DSP_AT:

   @allure.id("62334")
   @allure.title("Выполнение теста №1")   
   def test_AT_task1(self, LX_connection): 
      with allure.step("запуск файла по ssh на удаленной машине LNX"):
         result = LX_connection.run_test_ssh_1()
         logging.info(f"Результат выполнения файла по ssh: {result}")
         check.equal(result, "Hello, World!\n", "test_AT_task1 failed")
         # ПРОВЕРКА ОТВЕТА ОТ LW без подключенного АСРВ
      with allure.step("Установка соединения с программой LabVIEW"):
         answer = data_transfer_with_VI(labview_connection, device_info, test_name=HF_Test.Singletone)
         logging.info(f"Ответ от LabVIEW: {answer}")
         check.equal(answer, "ERR_-1", "Something doesnt work right")
         
   
   @allure.id("62328")
   @allure.title("Выполнение теста №2")
   def test_AT_task2(self, LX_connection):
      with allure.step("выполнение команды по ssh (ls) удаленной машине LNX"):
         result = LX_connection.run_test_ssh_2()
         logging.info(f"Результат выполнения файла по ssh: {result}")
         check.equal(result, "snap\n", "test_AT_task2 failed")
         # ПРОВЕРКА ОТВЕТА ОТ LW без подключенного АСРВ
      with allure.step("Установка соединения с программой LabVIEW"):
         answer = data_transfer_with_VI(labview_connection, device_info, test_name=HF_Test.Loopback)
         logging.info(f"Ответ от LabVIEW: {answer}")
         check.equal(answer, "ERR_-1", "Something doesnt work right")
      




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