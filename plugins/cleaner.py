import os
import glob

def clear_allure_results():
    """Удаляет только файлы результатов, сохраняя метаданные"""
    files = glob.glob("allure-results/*")
    for f in files:
        if not f.endswith(".yml"):  # Сохраняем YAML-файлы (метаданные)
            os.remove(f)