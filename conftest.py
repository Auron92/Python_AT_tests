import allure
import pytest
import paramiko
import logging
from configs.configurations import allure_upload
from configs.connections import LX
from configs.configurations import device_info
import os
import shutil
import subprocess
import time


@pytest.fixture(autouse=True)
def log_test_duration(request):
    start_time = time.time()
    yield
    duration = time.time() - start_time
    logging.info(f"Тест {request.node.name} выполнен за {duration:.2f} сек")
    allure.attach(f"Duration: {duration:.2f}s", name="Время выполнения", attachment_type=allure.attachment_type.TEXT)


@pytest.fixture(scope="session")  
def LX_connection():
    try:
        lx = LX()
        lx.create_ssh_connection()
        yield lx
        lx.close_ssh_connection()
    except paramiko.AuthenticationException as e:
        yield "FAILED"





# АВТОМАТИЧЕСКАЯ ЗАГРУЗКА В ALLURE с STW-PRO-TEST

# pytest_plugins = [
#     'stw_pro_test.uploader.allure',
#     'stw_pro_test.hooks.configure',
# ]    




# АВТОМАТИЧЕСКАЯ ЗАГРУЗКА В ALLURE по окончании всех тестов

def pytest_sessionfinish(session, exitstatus):
    print("⏩ Начинаю генерацию отчета для Allure...")
    """Вызывается после завершения всех тестов"""
    # Получаем настройки из файла конфигурации
    allurectl_path = allure_upload['allurectl_path']
    allure_endpoint = allure_upload['endpoint']
    allure_token = allure_upload['token']
    project_id = allure_upload['project_id']
    launch_name = allure_upload['launch_name']
    
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
        f"--launch-name={launch_name}",
        f"--launch-tags={device_info}"
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
        