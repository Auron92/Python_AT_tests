import pytest

if __name__ == "__main__":
    print("🚀 Запускаю проверки МЦОС АТ")
    if not(pytest.main(["test_DSP_AT.py", "-v", "-s", "-m only_interfaces"])):
        print("✅ Все тесты выполнены успешно")
    else:
        print("❌ Есть ошибки в тестах")