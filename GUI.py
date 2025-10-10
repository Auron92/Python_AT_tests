
import customtkinter as ctk
import threading
import time
import random
from tkinter import messagebox
import subprocess
from os import path
# Настройка внешнего вида
ctk.set_appearance_mode("Dark")  # "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class TestMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🚀 Автоматизированное тестирование МЦОС АТ")
        self.geometry("700x400")
        
        self.create_widgets()


    def create_widgets(self):
        # Главный контейнер
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок
        header = ctk.CTkFrame(main_container, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header,
            text="🚀 Автоматизированное тестирование МЦОС АТ",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack()

        frame_for_tests = ctk.CTkFrame(main_container,fg_color="#272726",width=500,height=230)
        frame_for_tests.place(x=50, y=60)

        test_button_1 = ctk.CTkButton(
            frame_for_tests,
            text="▶ Запустить полный тест",
            command=self.run_full_test,
            fg_color="#2E8B57",
            hover_color="#2EB76E",
            width=300,
            height=40
        )
        test_button_1.grid(row=0, column=0, padx=10, pady=10, ipadx=0, ipady=0)

        self.indicator_1 = ctk.CTkFrame(frame_for_tests, width=30, height=30, fg_color="#C3C8C6")
        self.indicator_1.pack_propagate(False)  # Запрещаем изменение размера
        self.indicator_1.configure(corner_radius=4)  # Слегка скругленные углы
        self.indicator_1.grid(row=0, column=1, padx=10, pady=10, ipadx=0, ipady=0)

        test_button_2 = ctk.CTkButton(
            frame_for_tests,
            text="▶ Запустить только ВЧ-тесты",
            command=self.run_hf_tests,
            fg_color="#2E8B57",
            hover_color="#2EB76E",
            width=300,
            height=40
        )
        test_button_2.grid(row=1, column=0, padx=10, pady=10, ipadx=0, ipady=0)

        self.indicator_2 = ctk.CTkFrame(frame_for_tests, width=30, height=30, fg_color="#C3C8C6")
        self.indicator_2.pack_propagate(False)  # Запрещаем изменение размера
        self.indicator_2.configure(corner_radius=4)  # Слегка скругленные углы
        self.indicator_2.grid(row=1, column=1, padx=10, pady=10, ipadx=0, ipady=0)


        test_button_3 = ctk.CTkButton(
            frame_for_tests,
            text="▶ Запустить только тесты интерфейсов",
            command=self.run_interfaces_tests,
            fg_color="#2E8B57",
            hover_color="#2EB76E",
            width=300,
            height=40
        )
        test_button_3.grid(row=2, column=0, padx=10, pady=10, ipadx=0, ipady=0)

        self.indicator_3 = ctk.CTkFrame(frame_for_tests, width=30, height=30, fg_color="#C3C8C6")
        self.indicator_3.pack_propagate(False)  # Запрещаем изменение размера
        self.indicator_3.configure(corner_radius=4)  # Слегка скругленные углы
        self.indicator_3.grid(row=2, column=1, padx=10, pady=10, ipadx=0, ipady=0)

        self.main_label = ctk.CTkLabel(frame_for_tests, width=170, height=150, fg_color="#C3C8C6", text='')
        self.main_label.grid(row=0, column=2, rowspan=3, padx=10, pady=10, ipadx=0, ipady=0)
        self.main_label.configure(corner_radius=7, text_color="#000302", anchor="nw", justify="left", wraplength=125)
        

    def run_full_test(self):
        result = subprocess.run(['pytest', "test_DSP_AT.py", "-v", "-s"])
        if not(result.returncode):
            self.main_label.configure(text="✅ Все тесты выполнены успешно")
            self.indicator_1.configure(fg_color="#2AC734")
            
        else:
            self.main_label.configure(text="❌ Есть ошибки в тестах")
            self.indicator_1.configure(fg_color="#EB4629")
            

    def run_hf_tests(self):
        result = subprocess.run(['pytest', "test_DSP_AT.py", "-v", "-s", "-m hf"])
        if not(result.returncode):
            self.main_label.configure(text="✅ Все тесты выполнены успешно")
            self.indicator_2.configure(fg_color="#2AC734")
            
        else:
            self.main_label.configure(text="❌ Есть ошибки в тестах")
            self.indicator_2.configure(fg_color="#EB4629")
            

    
    def run_interfaces_tests(self):
        result = subprocess.run(['pytest', "test_DSP_AT.py", "-v", "-s", "-m only_interfaces"])
        if not(result.returncode):
            self.main_label.configure(text="✅ Все тесты выполнены успешно")
            self.indicator_3.configure(fg_color="#2AC734")
            
        else:
            self.main_label.configure(text="❌ Есть ошибки в тестах")
            self.indicator_3.configure(fg_color="#EB4629")


#ЧТЕНИЕ ФАЙЛА test.log

# ini_path = path.dirname(path.abspath(__file__))
# ini_path = path.join(ini_path, 'logs')
# ini_path = path.join(ini_path, 'test.log')
# with open(ini_path, "r", encoding="utf-8") as file:
#     content = file.read()



if __name__ == "__main__":
    app = TestMonitorApp()
    app.mainloop()     


