import pytest_check as check
import pytest
import logging
from configs.TCP_client_LabVIEW_Python_connection_DSP_AT import data_transfer_with_VI
from configs.configurations import labview_connection
from configs.TCP_client_LabVIEW_Python_connection_DSP_AT import HF_Test
import os

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


class Tests_DSP_AT:
      
   def test_DSP_AT(self, LX_connection): 
      result = LX_connection.run_tests_LX()
      # Обработка ответа, парсинг лога и проверка значений с ожидаемыми результатами
      check.equal(result, ".....", "test_DSP_AT failed")

   def test_FPGA(self, LX_connection): 
      result = LX_connection.run_tests_FPGA()
      # Обработка ответа, парсинг лога и проверка значений с ожидаемыми результатами
      check.equal(result, ".....", "test_DSP_AT failed")

   def test_hw_Singletone(self, LX_connection):
      LX_connection.run_hw_test_Singletone()
      answer = data_transfer_with_VI(labview_connection, "Device_name", test_name=HF_Test.Singletone)
      response_processing_from_Labview(answer, "Singletone")
   
   def test_hw_Phaseshift(self, LX_connection):
      LX_connection.run_hw_test_Phaseshift()
      answer = data_transfer_with_VI(labview_connection, "Device_name", test_name=HF_Test.Phaseshift)
      response_processing_from_Labview(answer, "Phaseshift")

   def test_hw_Freqresp(self, LX_connection):
      LX_connection.run_hw_test_Freqresp()
      answer = data_transfer_with_VI(labview_connection, "Device_name", test_name=HF_Test.Freqresp)
      response_processing_from_Labview(answer, "Freqresp")

   def test_hw_Loopback(self, LX_connection):
      LX_connection.run_hw_test_Loopback()
      answer = data_transfer_with_VI(labview_connection, "Device_name", test_name=HF_Test.Loopback)
      response_processing_from_Labview(answer, "Loopback")