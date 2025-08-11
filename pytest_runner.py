import pytest


if __name__ == "__main__":
    
    if not(pytest.main(["test_DSP_AT_for_testing.py", "-v"])):
        print("✅ Все тесты выполнены успешно")
    else:
        print("❌ Есть ошибки в тестах")