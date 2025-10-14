#### 1.⚙️ Заполнение файла config.ini --->

[***server***] - Введите ip, port  Linux-модуля LX

[***user***] - Введите креды ддя подлючения к Linux-модулю LX по SSH

[***device***] - Введите в поле [sn] номер платы МЦОС АТ, эти данные передаются в LabVIEW для
сохранения логов, а так же в тэги в Allure TestOps.

[___Labview_connection___] - Введите в поле [host] IP-адрес ПК, на котором запущена программа LabVIEW
"DSP_AT_RF_Testing", а в поле [port] - номер порта, который указан на лицевой панели программы LabVIEW с подписью "PORT FOR CONNECTION TO THIS VI"

[___Allure___] - Введите в поле [launch_name] название конретного запуска проверки, который будет отображаться в Allure.

***Сохраните config.ini (Ctrl+S или File -> Save)***

#### 2.🚀 Запуск проверок

##### ***ПРОВЕРКА ИНТЕРФЕЙСОВ МЦОС АТ***

```sh {"background":"false","name":"ЗАПУСК ПРОВЕРОК ИНТЕРФЕЙСОВ МЦОС АТ"}
python runners//run_tests_interfaces_DSP_AT.py
Write-Host '=== ВЫПОЛНЕНИЕ ЗАВЕРШЕНО ===' -ForegroundColor Green
Start-Sleep -s 2
```

##### ***ПРОВЕРКА ВЧ МЦОС АТ***

```sh {"background":"false","name":"ЗАПУСК ВЧ ПРОВЕРОК МЦОС АТ"}
python runners//run_HF_tests_DSP_AT.py
Write-Host '=== ВЫПОЛНЕНИЕ ЗАВЕРШЕНО ===' -ForegroundColor Green
Start-Sleep -s 2
```

##### ***ПОЛНАЯ ПРОВЕРКА МЦОС АТ***

```sh {"background":"false","name":"ЗАПУСК ПОЛНОЙ ПРОВЕРКИ МЦОС АТ"}
python runners//run_full_test_DSP_AT.py
Write-Host '=== ВЫПОЛНЕНИЕ ЗАВЕРШЕНО ===' -ForegroundColor Green
Start-Sleep -s 2
```

##### ***ALLURE TESTOPS***

Результаты выполнения тестов выгружаются в Allure TestOps -  ***https://allure.1440.space/project/131/launches***

#### Заметки

(Замечено, что периодически вылетает ошибка таймаута при выгрузке в Allure, желательно открыть в браузере Allure TestOps и залогиниться https://allure.1440.space/project/131/launches)

(В идеале, наверное, сначала на коротком тесте проверить выгрузку, и дальше уже можно любые проверки запускать пока открыт VSCode)

(full-test длится около 35 минут, самый продолжительный по времени - test-fpga)
