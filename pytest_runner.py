import pytest
from configs.configurations import TEST_TYPE

if __name__ == "__main__":

    if TEST_TYPE == 'short':    
        if not(pytest.main(["test_DSP_AT.py", "-v", "-s", "-m only_interfaces"])):
            print("✅ Все тесты выполнены успешно")
        else:
            print("❌ Есть ошибки в тестах")

    elif TEST_TYPE == 'full':    
        if not(pytest.main(["test_DSP_AT.py", "-v", "-s"])):
            print("✅ Все тесты выполнены успешно")
        else:
            print("❌ Есть ошибки в тестах")

    else:
        print("В файле config.ini введите корректно test_type")