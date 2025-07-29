from colorlog import ColoredFormatter
import pytest
import paramiko
import logging
from configs.configurations import server_auth
from configs.connections import LX
import os
import shutil
import subprocess
from datetime import datetime


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
    
    # Создаём папку для логов, если её нет
    os.makedirs("logs", exist_ok=True)
    
    # Настройка файлового логгера (без цветов)
    file_handler = logging.FileHandler("logs/test.log", mode='w')
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # Простой формат
    )
    logging.getLogger().addHandler(file_handler)

# АВТОМАТИЧЕСКАЯ ЗАГРУЗКА В ALLURE с STW-PRO-TEST

# pytest_plugins = [
#     'stw_pro_test.uploader.allure',
#     'stw_pro_test.hooks.configure',
# ]    




# АВТОМАТИЧЕСКАЯ ЗАГРУЗКА В ALLURE

def pytest_sessionfinish(session, exitstatus):
    """Вызывается после завершения всех тестов"""
    # Получаем настройки из переменных окружения
    allurectl_path = "C:\\Users\\m.maltsev\\Desktop\\Work_Files\\allurectl_windows_amd64.exe"
    allure_endpoint = "https://allure.1440.space/"
    allure_token = "5d332763-7646-455c-b593-cfefa5a725ab"
    project_id = "131"  # Значение по умолчанию
    
    # Генерируем имя запуска с timestamp
    launch_name = f"Automated Run {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    
    # Если указаны креды, авторизуемся
    if allure_endpoint and allure_token:
        auth_cmd = [
            allurectl_path,
            "auth",
            "login",
            f"--endpoint={allure_endpoint}",
            f"--token={allure_token}"
        ]
        try:
            subprocess.run(auth_cmd, check=True)
        except subprocess.CalledProcessError as e:
            pytest.exit(f"Allure TestOps auth failed: {e}")

    # Команда для загрузки результатов
    upload_cmd = [
        allurectl_path,
        "upload",
        "allure-results",
        f"--project-id={project_id}",
        f"--launch-name={launch_name}"
    ]

    try:
        # Выполняем загрузку
        subprocess.run(upload_cmd, check=True)
        print(f"\nAllure results uploaded to TestOps. Launch: {launch_name}")
    except subprocess.CalledProcessError as e:
        print(f"\nFailed to upload results to Allure TestOps: {e}")
    except FileNotFoundError:
        print("\nallurectl not found. Install it from https://github.com/allure-framework/allurectl")

    # Очищаем результаты (опционально)
    if os.path.exists("allure-results"):
        shutil.rmtree("allure-results")