    

def parsing_log_test_fpga(response):
    steps = response.split("\n")
    filtered_steps = [step for step in steps if "OK" in step or "FAIL" in step]

    test_names = []    # Часть до "OK"/"FAIL"
    additional_info = []  # Часть после "OK"/"FAIL" (если есть)
    test_status = []

    for line in filtered_steps:
        if "OK" in line:
            parts = line.split("OK", 1)
            status = "OK"
        else:
            parts = line.split("FAIL", 1)
            status = "FAIL"
        
        # Чистим части от лишних пробелов и символов
        name = parts[0].strip(" :")  # Удаляем двоеточия и пробелы по краям
        info = parts[1].strip(" .") if len(parts) > 1 else ""  # Удаляем точки/пробелы
        
        # Добавляем в списки
        test_names.append(f"{name}")
        additional_info.append(info if info else "No additional info")
        test_status.append(f"{status}")
    # Вывод результатов
    # print("Test Names:", test_names)
    # print("Test_status:", test_status)
    # print("Additional Info:", additional_info)
    return test_names, test_status, additional_info



def parsing_log_from_test_log_file(response):
    steps = response.split("\n")
    filtered_steps = [step for step in steps if "OK" in step or "FAIL" in step]

    test_names = []    # Часть до "OK"/"FAIL"
    test_status = []

    for line in filtered_steps:
        if "OK" in line:
            parts = line.split("OK", 1)
            status = "OK"
        else:
            parts = line.split("FAIL", 1)
            status = "FAIL"
        
        # Чистим части от лишних пробелов и символов
        name = parts[0].strip(" :")  # Удаляем двоеточия и пробелы по краям
        
        # Добавляем в списки
        test_names.append(f"{name}")
        test_status.append(f"{status}")
    # Вывод результатов
    # print("Test Names:", test_names)
    # print("Test_status:", test_status)
    # print("Additional Info:", additional_info)
    return test_names, test_status