import customtkinter as ctk
import threading
import time
import random
from tkinter import messagebox

# Настройка внешнего вида
ctk.set_appearance_mode("Dark")  # "Light", "Dark", "System"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

class TestMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("🧪 Монитор выполнения тестов")
        self.geometry("1000x600")
        self.minsize(900, 500)
        
        # Список тестов
        self.tests = [
            {"name": "Тест авторизации", "status": "waiting", "duration": 0},
            {"name": "Тест корзины покупок", "status": "waiting", "duration": 0},
            {"name": "Тест поиска товаров", "status": "waiting", "duration": 0},
            {"name": "Тест оформления заказа", "status": "waiting", "duration": 0},
            {"name": "Тест платежной системы", "status": "waiting", "duration": 0},
            {"name": "Тест уведомлений", "status": "waiting", "duration": 0},
            {"name": "Тест производительности", "status": "waiting", "duration": 0},
            {"name": "Тест безопасности", "status": "waiting", "duration": 0}
        ]
        
        self.currently_running = None
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
            text="🧪 Мониторинг выполнения тестов",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            header,
            text="Реальный мониторинг статуса автоматизированных тестов",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle.pack(pady=(5, 0))
        
        # Панель управления
        control_frame = ctk.CTkFrame(main_container)
        control_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            control_frame,
            text="Управление тестированием:",
            font=ctk.CTkFont(weight="bold")
        ).pack(pady=(15, 10))
        
        btn_container = ctk.CTkFrame(control_frame, fg_color="transparent")
        btn_container.pack(pady=10)
        
        start_all_btn = ctk.CTkButton(
            btn_container,
            text="▶ Запустить все тесты",
            command=self.start_all_tests,
            fg_color="#2E8B57",
            hover_color="#3CB371",
            width=150,
            height=40
        )
        start_all_btn.pack(side="left", padx=5)
        
        stop_all_btn = ctk.CTkButton(
            btn_container,
            text="⏹ Остановить все",
            command=self.stop_all_tests,
            fg_color="#DC143C",
            hover_color="#FF4500",
            width=150,
            height=40
        )
        stop_all_btn.pack(side="left", padx=5)
        
        clear_btn = ctk.CTkButton(
            btn_container,
            text="🗑️ Очистить результаты",
            command=self.clear_results,
            fg_color="#696969",
            hover_color="#808080",
            width=150,
            height=40
        )
        clear_btn.pack(side="left", padx=5)
        
        # Список тестов
        list_frame = ctk.CTkFrame(main_container)
        list_frame.pack(fill="both", expand=True, pady=10)
        
        # Заголовки колонок
        header_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(header_frame, text="Тест", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(20, 0))
        ctk.CTkLabel(header_frame, text="Статус", font=ctk.CTkFont(weight="bold")).pack(side="right", padx=(0, 150))
        ctk.CTkLabel(header_frame, text="Действия", font=ctk.CTkFont(weight="bold")).pack(side="right", padx=(0, 20))
        
        # Контейнер для списка тестов с прокруткой
        self.canvas = ctk.CTkCanvas(list_frame, bg="#2B2B2B", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(list_frame, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas, fg_color="transparent")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Привязка колесика мыши к прокрутке
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self.on_mousewheel)
        
        # Создаем строки для каждого теста
        self.test_widgets = []
        for i, test in enumerate(self.tests):
            self.create_test_row(test, i)
        
        # Статистика
        stats_frame = ctk.CTkFrame(main_container)
        stats_frame.pack(fill="x", pady=10)
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Всего тестов: 8 | Ожидание: 8 | Выполняется: 0 | Успешно: 0 | С ошибкой: 0",
            font=ctk.CTkFont(size=12)
        )
        self.stats_label.pack(pady=10)
        
        # Строка состояния
        self.create_status_bar(main_container)
        
    def create_test_row(self, test, index):
        """Создает строку для отображения теста"""
        row_frame = ctk.CTkFrame(self.scrollable_frame, height=60)
        row_frame.pack(fill="x", padx=10, pady=5)
        row_frame.pack_propagate(False)
        
        # Название теста
        name_label = ctk.CTkLabel(
            row_frame,
            text=test["name"],
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        name_label.place(x=20, y=20, anchor="w")
        
        # Индикатор статуса
        status_indicator = ctk.CTkLabel(
            row_frame,
            text="●",
            font=ctk.CTkFont(size=20),
            text_color="gray"  # серый - ожидание
        )
        status_indicator.place(relx=0.7, y=20, anchor="center")
        
        status_text = ctk.CTkLabel(
            row_frame,
            text="Ожидание",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        status_text.place(relx=0.7, y=40, anchor="center")
        
        # Кнопка запуска
        start_btn = ctk.CTkButton(
            row_frame,
            text="Запуск",
            width=80,
            height=30,
            command=lambda t=test: self.start_test(t)
        )
        start_btn.place(relx=0.85, y=20, anchor="center")
        
        # Сохраняем виджеты для обновления
        test_widget = {
            "frame": row_frame,
            "name_label": name_label,
            "indicator": status_indicator,
            "status_text": status_text,
            "start_btn": start_btn
        }
        
        self.test_widgets.append(test_widget)
        
    def create_status_bar(self, parent):
        """Создает строку состояния"""
        status_bar = ctk.CTkFrame(parent, height=30, corner_radius=0)
        status_bar.pack(fill="x", side="bottom", pady=(20, 0))
        
        # Статус системы
        self.status_message = ctk.CTkLabel(
            status_bar,
            text="✅ Система готова к работе. Выберите тест для запуска.",
            font=ctk.CTkFont(size=12)
        )
        self.status_message.pack(side="left", padx=10)
        
        # Информация о системе
        info_frame = ctk.CTkFrame(status_bar, fg_color="transparent")
        info_frame.pack(side="right", padx=10)
        
        ctk.CTkLabel(
            info_frame,
            text="Тест монитор v1.0 | © 2024",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        ).pack(side="right", padx=5)
        
    def update_test_status(self, test, status, color, text):
        """Обновляет статус теста в интерфейсе"""
        index = self.tests.index(test)
        widgets = self.test_widgets[index]
        
        widgets["indicator"].configure(text_color=color)
        widgets["status_text"].configure(text=text, text_color=color)
        
        # Обновляем статистику
        self.update_stats()
        
    def update_stats(self):
        """Обновляет статистику тестов"""
        total = len(self.tests)
        waiting = sum(1 for t in self.tests if t["status"] == "waiting")
        running = sum(1 for t in self.tests if t["status"] == "running")
        success = sum(1 for t in self.tests if t["status"] == "success")
        error = sum(1 for t in self.tests if t["status"] == "error")
        
        self.stats_label.configure(
            text=f"Всего тестов: {total} | Ожидание: {waiting} | Выполняется: {running} | Успешно: {success} | С ошибкой: {error}"
        )
        
    def update_status_message(self, message):
        """Обновляет сообщение в строке состояния"""
        self.status_message.configure(text=message)
        
    def start_test(self, test):
        """Запускает отдельный тест"""
        if test["status"] == "running":
            messagebox.showwarning("Внимание", f"Тест '{test['name']}' уже выполняется!")
            return
            
        test["status"] = "running"
        self.update_test_status(test, "running", "orange", "Выполняется...")
        self.update_status_message(f"🟠 Выполняется: {test['name']}")
        self.currently_running = test["name"]
        
        # Запуск в отдельном потоке
        thread = threading.Thread(target=self.execute_test, args=(test,), daemon=True)
        thread.start()
        
    def start_all_tests(self):
        """Запускает все тесты по очереди"""
        for test in self.tests:
            if test["status"] == "waiting":
                self.start_test(test)
                time.sleep(0.5)  # Небольшая задержка между запусками
        
    def stop_all_tests(self):
        """Останавливает все выполняющиеся тесты"""
        for test in self.tests:
            if test["status"] == "running":
                test["status"] = "waiting"
                self.update_test_status(test, "waiting", "gray", "Остановлен")
                
        self.update_status_message("⏹ Все тесты остановлены")
        self.currently_running = None
        
    def clear_results(self):
        """Очищает все результаты тестов"""
        for test in self.tests:
            test["status"] = "waiting"
            test["duration"] = 0
            self.update_test_status(test, "waiting", "gray", "Ожидание")
            
        self.update_status_message("🧹 Результаты тестов очищены")
        self.update_stats()
        
    def execute_test(self, test):
        """Имитирует выполнение теста"""
        try:
            # Случайная длительность теста 2-8 секунд
            duration = random.uniform(2.0, 8.0)
            start_time = time.time()
            
            # Имитация работы теста
            while time.time() - start_time < duration:
                if test["status"] != "running":
                    return
                time.sleep(0.1)
            
            # Определяем результат (80% успеха, 20% ошибки)
            success = random.random() < 0.8
            
            if success:
                test["status"] = "success"
                self.after(0, lambda: self.update_test_status(test, "success", "green", "Успешно"))
                self.after(0, lambda: self.update_status_message(f"✅ {test['name']} выполнен успешно!"))
            else:
                test["status"] = "error"
                self.after(0, lambda: self.update_test_status(test, "error", "red", "Ошибка"))
                self.after(0, lambda: self.update_status_message(f"❌ {test['name']} завершен с ошибкой!"))
                
            test["duration"] = time.time() - start_time
            
        except Exception as e:
            self.after(0, lambda: self.update_test_status(test, "error", "red", "Ошибка"))
            self.after(0, lambda: self.update_status_message(f"❌ Ошибка в {test['name']}: {str(e)}"))
            
    def on_mousewheel(self, event):
        """Обработка прокрутки колесиком мыши"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

if __name__ == "__main__":
    app = TestMonitorApp()
    app.mainloop()