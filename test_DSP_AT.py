import allure
import pytest_check as check
import pytest
import logging
from configs.TCP_client_LabVIEW_Python_connection_DSP_AT import data_transfer_with_VI
from configs.configurations import labview_connection
from configs.TCP_client_LabVIEW_Python_connection_DSP_AT import HF_Test
from parsing_logs_from_LX import parsing_log_test_fpga
from parsing_logs_from_LX import parsing_log_from_test_log_file
from configs.configurations import device_info
import os


@allure.id('62327')
@allure.label("owner", "m.maltsev")
@pytest.mark.only_interfaces
@pytest.mark.hf
@allure.description("Выполнение подключения к linux-server по SSH")
def test_authentication(LX_connection):
   if LX_connection == 'FAILED':
      print("❌ Аутентификация провалена! Аварийный выход.")
      os._exit(1)
   else:
      logging.info("✅ Аутентификация завершена!")
      assert "Auth complete!"
      
def response_processing_from_Labview(answ, testname: str):
   logging.info(f"{testname}:{answ}")
   res = answ.split(';')
   result = res[0]
   check.equal(result, 'ok', f'Test {testname} failed')
   if result == 'ok':
      logging.info(f'Test {testname} success')
   elif result == 'fail':
      logging.error(f'Test {testname} fail')
   elif result == 'no_signal':
      logging.error(f'Test {testname} no_signal')
   else:
      logging.error('Labview dont answer')


@allure.feature("DSP_AT")
class Tests_DSP_AT:

   
   @allure.id('63666')
   @allure.label("owner", "m.maltsev")
   @pytest.mark.only_interfaces
   @allure.description("Проверка интерфейсов МЦОС АТ")
   @allure.title("Проверка test-interfaces")   
   def test_interfaces(self, LX_connection): 
      result = LX_connection.run_tests_LX()
      # Обработка ответа, парсинг лога и проверка значений с ожидаемыми результатами
      test_names, test_statuses = parsing_log_from_test_log_file(result)
      for test_name, test_status in zip(test_names, test_statuses):
         with allure.step(f"{test_name}"):
            logging.info(f"{test_name} result: {test_status}")
            check.equal(test_status, 'OK', f"{test_name} failed")

   @allure.id('63622')
   @allure.label("owner", "m.maltsev")
   @allure.description("Проверка ПЛИС МЦОС АТ")
   @allure.title("Проверка test-fpga")  
   def test_FPGA(self, LX_connection): 
      result = LX_connection.run_tests_FPGA()
      logging.info(f"{result}")
      logging.info("---------------ОБРАБОТКА ОТВЕТА от ПЛИС---------------")
      # Обработка ответа, парсинг лога и проверка значений с ожидаемыми результатами
      test_names, test_statuses, additional_infos = parsing_log_test_fpga(result)
      for test_name, test_status, additional_info in zip(test_names, test_statuses, additional_infos):
         with allure.step(f"{test_name}"):
            logging.info(f"{test_name} result: {test_status}")
            check.equal(test_status, 'OK', f"{test_name} failed")
            logging.info(f"{test_name} Additional info: {additional_info}")

   @allure.id('62331')
   @allure.label("owner", "m.maltsev")
   @pytest.mark.hf
   @allure.description("Проверка SINGLETONE ВЧ-теста")
   @allure.title("Проверка test_hf_Singletone") 
   def test_hw_Singletone(self, LX_connection):
      with allure.step("Отправка команды на включение режима проверки"):
         result = LX_connection.run_hw_test_Singletone()
         logging.info(f"{result}")
         check.is_in("SINGLETONE", result, "Ответа нет, тест не включен")
      with allure.step("Подключение к программе LabVIEW и выполнение измерений"):
         answer = data_transfer_with_VI(labview_connection, device_info, test_name=HF_Test.Singletone)
         response_processing_from_Labview(answer, "Singletone")
   
   @allure.id('62333')
   @allure.label("owner", "m.maltsev")
   @pytest.mark.hf
   @allure.description("Проверка PHASESHIFT ВЧ-теста")
   @allure.title("Проверка test_hf_Phaseshift") 
   def test_hw_Phaseshift(self, LX_connection):
      with allure.step("Отправка команды на включение режима проверки"):
         result = LX_connection.run_hw_test_Phaseshift()
         logging.info(f"{result}")
         check.is_in("PHASESHIFT", result, "Ответа нет, тест не включен")
      with allure.step("Подключение к программе LabVIEW и выполнение измерений"):
         answer = data_transfer_with_VI(labview_connection, device_info, test_name=HF_Test.Phaseshift)
         response_processing_from_Labview(answer, "Phaseshift")

   @allure.id('62329')
   @allure.label("owner", "m.maltsev")
   @pytest.mark.hf
   @allure.description("Проверка FREQRESP ВЧ-теста")
   @allure.title("Проверка test_hf_Freqresp") 
   def test_hw_Freqresp(self, LX_connection):
      with allure.step("Отправка команды на включение режима проверки"):
         result = LX_connection.run_hw_test_Freqresp()
         logging.info(f"{result}")
         check.is_in("FREQRESP", result, "Ответа нет, тест не включен")
      with allure.step("Подключение к программе LabVIEW и выполнение измерений"):
         answer = data_transfer_with_VI(labview_connection, device_info, test_name=HF_Test.Freqresp)
         response_processing_from_Labview(answer, "Freqresp")

   @allure.id('62330')
   @allure.label("owner", "m.maltsev")
   @pytest.mark.hf
   @allure.description("Проверка LOOPBACK ВЧ-теста")
   @allure.title("Проверка test_hf_Loopback")
   def test_hw_Loopback(self, LX_connection):
      with allure.step("Отправка команды на включение режима проверки"):
         result = LX_connection.run_hw_test_Loopback()
         logging.info(f"{result}")
         check.is_in("LOOPBACK", result, "Ответа нет, тест не включен")
      with allure.step("Подключение к программе LabVIEW и выполнение измерений"):   
         answer = data_transfer_with_VI(labview_connection, device_info, test_name=HF_Test.Loopback)
         response_processing_from_Labview(answer, "Loopback")


