import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLineEdit, QLabel,
    QComboBox, QSpinBox, QCheckBox, QVBoxLayout, QWidget, QFileDialog, QProgressBar,
    QSystemTrayIcon, QMenu, QHBoxLayout, QTimeEdit
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt, QTimer, QSize, QTime, QDateTime
from VKMessengerWorker import VKMessengerWorker
from themes import get_global_style, get_title_style, get_input_style, get_checkbox_style, get_author_label_style
import datetime

CONFIG_PATH = "config.json"
LOG_FILE = "log.txt"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.next_launch = None  # Инициализация переменной для следующего автозапуска

        # Устанавливаем иконку приложения
        app_icon_path = "icons/icon.ico"
        if os.path.exists(app_icon_path):
            self.setWindowIcon(QIcon(app_icon_path))
        else:
            print(f"Иконка приложения не найдена: {app_icon_path}")

        # Интерфейс
        self.setWindowTitle("VK Messenger Automation V4")
        self.setStyleSheet(get_global_style())
        self.setGeometry(100, 100, 400, 600)

        # Центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout(central_widget)

        # Заголовок и иконка сворачивания в трей
        header_layout = QHBoxLayout()
        self.title_label = QLabel("VK Messenger Automation V4", self)
        self.title_label.setStyleSheet(get_title_style())
        header_layout.addWidget(self.title_label)

        tray_icon_path = "icons/tray_icon.png"
        if os.path.exists(tray_icon_path):
            self.tray_icon_label = QLabel(self)
            self.tray_icon_label.setPixmap(QIcon(tray_icon_path).pixmap(24, 24))
            self.tray_icon_label.setCursor(Qt.PointingHandCursor)
            self.tray_icon_label.mousePressEvent = self.minimize_to_tray
            header_layout.addWidget(self.tray_icon_label)
        else:
            print(f"Иконка для сворачивания в трей не найдена: {tray_icon_path}")

        layout.addLayout(header_layout)

        # Поля ввода
        self.chat_id_input = QLineEdit(self)
        self.chat_id_input.setPlaceholderText("Введите ID чата")
        self.chat_id_input.setStyleSheet(get_input_style())
        layout.addWidget(self.chat_id_input)

        self.user_data_dir_input = QLineEdit(self)
        self.user_data_dir_input.setPlaceholderText("Выберите папку профиля Chrome")
        self.user_data_dir_input.setStyleSheet(get_input_style())
        layout.addWidget(self.user_data_dir_input)

        # Кнопка выбора папки профиля Chrome
        self.user_data_dir_button = QPushButton("Выбрать папку", self)
        self.user_data_dir_button.setFixedSize(320, 52)
        folder_icon_path = "icons/folder_icon.png"
        if os.path.exists(folder_icon_path):
            self.user_data_dir_button.setIcon(QIcon(folder_icon_path))
        else:
            print(f"Иконка не найдена: {folder_icon_path}")
        self.user_data_dir_button.setIconSize(QSize(20, 20))
        self.user_data_dir_button.clicked.connect(self.select_user_data_dir)
        layout.addWidget(self.user_data_dir_button)

        self.quotes_path_input = QLineEdit(self)
        self.quotes_path_input.setPlaceholderText("Выберите файл с цитатами")
        self.quotes_path_input.setStyleSheet(get_input_style())
        layout.addWidget(self.quotes_path_input)

        # Кнопка выбора файла с цитатами
        self.quotes_path_button = QPushButton("Выбрать файл", self)
        self.quotes_path_button.setFixedSize(320, 52)
        file_icon_path = "icons/file_icon.png"
        if os.path.exists(file_icon_path):
            self.quotes_path_button.setIcon(QIcon(file_icon_path))
        else:
            print(f"Иконка не найдена: {file_icon_path}")
        self.quotes_path_button.setIconSize(QSize(20, 20))
        self.quotes_path_button.clicked.connect(self.select_quotes_file)
        layout.addWidget(self.quotes_path_button)

        self.message_count_input = QSpinBox(self)
        self.message_count_input.setValue(5)
        self.message_count_input.setMinimum(1)
        self.message_count_input.setMaximum(50)
        self.message_count_input.setStyleSheet(get_input_style())
        layout.addWidget(self.message_count_input)

        self.interval_input = QSpinBox(self)
        self.interval_input.setValue(3)
        self.interval_input.setMinimum(1)
        self.interval_input.setMaximum(10)
        self.interval_input.setStyleSheet(get_input_style())
        layout.addWidget(self.interval_input)

        # Выбор дня недели
        self.day_of_week_combo = QComboBox(self)
        self.day_of_week_combo.addItems(
            ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"])
        self.day_of_week_combo.setStyleSheet(get_input_style())
        layout.addWidget(self.day_of_week_combo)

        # Выбор времени
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setStyleSheet(get_input_style())
        layout.addWidget(self.time_edit)

        # Кнопки "Обновить профили" и "Обновить конфигурацию" на одном уровне
        update_buttons_layout = QHBoxLayout()

        self.update_profiles_button = QPushButton("Обновить профили", self)
        self.update_profiles_button.setFixedSize(320, 52)
        profile_icon_path = "icons/profile_icon.png"
        if os.path.exists(profile_icon_path):
            self.update_profiles_button.setIcon(QIcon(profile_icon_path))
        else:
            print(f"Иконка не найдена: {profile_icon_path}")
        self.update_profiles_button.setIconSize(QSize(20, 20))
        self.update_profiles_button.clicked.connect(self.update_profile_list)
        update_buttons_layout.addWidget(self.update_profiles_button)

        self.update_config_button = QPushButton("Обновить конф.", self)
        self.update_config_button.setFixedSize(320, 52)
        config_icon_path = "icons/config_icon.png"
        if os.path.exists(config_icon_path):
            self.update_config_button.setIcon(QIcon(config_icon_path))
        else:
            print(f"Иконка не найдена: {config_icon_path}")
        self.update_config_button.setIconSize(QSize(20, 20))
        self.update_config_button.clicked.connect(self.save_settings)
        update_buttons_layout.addWidget(self.update_config_button)

        layout.addLayout(update_buttons_layout)

        # Выпадающий список профилей
        self.profile_combo = QComboBox(self)
        self.profile_combo.addItems(["Default"])
        self.profile_combo.setStyleSheet(get_input_style())
        layout.addWidget(self.profile_combo)

        self.save_settings_checkbox = QCheckBox("Запомнить настройки", self)
        self.save_settings_checkbox.setStyleSheet(get_checkbox_style())
        layout.addWidget(self.save_settings_checkbox)

        self.auto_launch_checkbox = QCheckBox("Автозапуск", self)
        self.auto_launch_checkbox.setStyleSheet(get_checkbox_style())
        layout.addWidget(self.auto_launch_checkbox)

        # Прогресс-бар
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("""
        QProgressBar {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid #4E8DF8;
            border-radius: 10px;
            text-align: center;
            color: #D1D5DB;
            font-family: 'Poppins', sans-serif;
            font-size: 14px;
        }
        QProgressBar::chunk {
            background-color: #56C6F2;
            border-radius: 10px;
        }
        """)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Кнопки "Отправить сообщения" и "Выход" на одном уровне
        buttons_layout = QHBoxLayout()

        self.send_button = QPushButton("Отправить сообщения", self)
        self.send_button.setFixedSize(320, 52)
        play_icon_path = "icons/play_icon.png"
        if os.path.exists(play_icon_path):
            self.send_button.setIcon(QIcon(play_icon_path))
        else:
            print(f"Иконка не найдена: {play_icon_path}")
        self.send_button.setIconSize(QSize(20, 20))
        self.send_button.clicked.connect(self.start_sending_messages)
        buttons_layout.addWidget(self.send_button)

        self.exit_button = QPushButton("Выход", self)
        self.exit_button.setFixedSize(320, 52)
        exit_icon_path = "icons/exit_icon.png"
        if os.path.exists(exit_icon_path):
            self.exit_button.setIcon(QIcon(exit_icon_path))
        else:
            print(f"Иконка не найдена: {exit_icon_path}")
        self.exit_button.setIconSize(QSize(20, 20))
        self.exit_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.exit_button)

        layout.addLayout(buttons_layout)

        # Статус-лейбл
        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet("color: #D1D5DB; font-family: 'Poppins', sans-serif; font-size: 14px;")
        layout.addWidget(self.status_label)

        # Авторский текст
        self.author_label = QLabel("Автор приложения: Сергей Каманов", self)
        self.author_label.setStyleSheet(get_author_label_style())
        layout.addWidget(self.author_label)

        # Настройка трея
        self.setup_tray_icon()

        # Загружаем настройки
        self.load_settings()

        # Проверка и автоматическое выполнение скрипта
        if self.auto_launch_checkbox.isChecked():
            self.check_and_run_script()

        # Запуск таймера для периодической проверки времени
        self.schedule_timer = QTimer(self)
        self.schedule_timer.timeout.connect(self.check_and_run_script)
        self.schedule_timer.start(60000)  # Проверка каждую минуту

    def setup_tray_icon(self):
        """Настройка иконки в трее."""
        self.tray_icon = QSystemTrayIcon(self)
        tray_icon_path = "icons/tray_icon.png"
        if os.path.exists(tray_icon_path):
            self.tray_icon.setIcon(QIcon(tray_icon_path))
        else:
            print(f"Иконка для трея не найдена: {tray_icon_path}")

        # Создаем меню для трея
        self.tray_menu = QMenu()
        restore_action = QAction("Развернуть", self)
        restore_action.triggered.connect(self.restore_from_tray)
        quit_action = QAction("Выход", self)
        quit_action.triggered.connect(self.close_application)
        self.tray_menu.addAction(restore_action)
        self.tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

    def closeEvent(self, event):
        """Перехватываем событие закрытия окна."""
        if self.tray_icon.isVisible():
            self.hide()  # Скрываем окно
            self.tray_icon.show()  # Показываем иконку в трее
            event.ignore()  # Игнорируем событие закрытия
        else:
            self.close_application()

    def close_application(self):
        """Полное закрытие приложения."""
        self.tray_icon.hide()
        QApplication.quit()

    def restore_from_tray(self):
        """Разворачиваем приложение из трея."""
        self.showNormal()
        self.activateWindow()

    def on_tray_icon_activated(self, reason):
        """Обработка активации иконки в трее."""
        if reason == QSystemTrayIcon.DoubleClick:
            self.restore_from_tray()

    def minimize_to_tray(self, event):
        """Сворачивает приложение в трей."""
        if event.button() == Qt.LeftButton:  # Проверяем, что нажата левая кнопка мыши
            self.hide()
            self.tray_icon.show()

    def select_user_data_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку профиля Chrome")
        if folder:
            self.user_data_dir_input.setText(folder)

    def select_quotes_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл с цитатами", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.quotes_path_input.setText(file_path)

    def start_sending_messages(self, automatic=False):
        chat_id = self.chat_id_input.text()
        user_data_dir = self.user_data_dir_input.text()
        quotes_path = self.quotes_path_input.text()
        message_count = self.message_count_input.value()
        interval = self.interval_input.value()
        profile = self.profile_combo.currentText()
        if not all([chat_id, user_data_dir, quotes_path]):
            self.status_label.setText("Пожалуйста, заполните все поля.")
            return
        if not os.path.isfile(quotes_path):
            self.status_label.setText("Выбранный файл с цитатами не существует.")
            return
        if self.save_settings_checkbox.isChecked():
            self.save_settings()
        # Блокируем кнопку "Отправить сообщения"
        self.send_button.setDisabled(True)
        self.send_button.setText("Отправка...")
        self.status_label.setText("Отправка сообщений...")
        self.worker = VKMessengerWorker(chat_id, user_data_dir, quotes_path, message_count, interval, profile)
        self.worker.automatic = automatic
        self.worker.finished.connect(self.update_status)
        self.worker.start()
        # Анимация прогресс-бара
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.timer.start(30)

    def update_progress(self):
        if self.progress_value < 100:
            self.progress_value += 1
            self.progress_bar.setValue(self.progress_value)
        else:
            self.timer.stop()

    def update_status(self, status):
        self.status_label.setText(status)
        self.progress_bar.setValue(0)
        # Разблокируем кнопку "Отправить сообщения" после завершения
        self.send_button.setEnabled(True)
        self.send_button.setText("Отправить сообщения")
        if self.worker.automatic:
            self.log_script_execution()

    def update_profile_list(self):
        """Обновляет список профилей в выпадающем меню."""
        user_data_dir = self.user_data_dir_input.text().strip()
        if not user_data_dir or not os.path.isdir(user_data_dir):
            self.status_label.setText("Укажите корректную папку профиля Chrome.")
            return
        profiles = self.scan_profiles(user_data_dir)
        if not profiles:
            self.status_label.setText("Профили не найдены.")
        else:
            self.profile_combo.clear()
            self.profile_combo.addItems(profiles)
            self.status_label.setText(f"Найдено {len(profiles)} профилей.")

    def scan_profiles(self, user_data_dir):
        """
        Сканирует папку профилей Chrome и возвращает список профилей,
        начинающихся на 'Default' или 'Profile'.
        :param user_data_dir: Путь к папке профиля Chrome.
        :return: Список найденных профилей.
        """
        if not os.path.exists(user_data_dir):
            return []
        profiles = []
        for folder in os.listdir(user_data_dir):
            if folder.startswith("Default") or folder.startswith("Profile"):
                profiles.append(folder)
        return profiles

    def load_settings(self):
        """Загружает настройки из config.json."""
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.chat_id_input.setText(data.get("chat_id", ""))
                    self.user_data_dir_input.setText(data.get("user_data_dir", ""))
                    self.quotes_path_input.setText(data.get("quotes_path", ""))
                    self.message_count_input.setValue(data.get("message_count", 5))
                    self.interval_input.setValue(data.get("interval", 3))
                    self.profile_combo.setCurrentText(data.get("profile", "Default"))
                    self.save_settings_checkbox.setChecked(data.get("remember", False))
                    self.auto_launch_checkbox.setChecked(data.get("auto_launch", False))
                    day_of_week = data.get("day_of_week", "Понедельник")
                    time_str = data.get("time", "00:00")
                    next_launch_str = data.get("next_launch", "")
                    self.day_of_week_combo.setCurrentText(day_of_week)
                    self.time_edit.setTime(QTime.fromString(time_str, "HH:mm"))
                    if next_launch_str:
                        self.next_launch = datetime.datetime.fromisoformat(next_launch_str)
                        # Проверяем, не прошло ли время next_launch
                        if self.next_launch < datetime.datetime.now():
                            self.update_next_launch()
                    else:
                        self.next_launch = None
            except Exception as e:
                print(f"Ошибка загрузки конфигурации: {e}")

    def save_settings(self):
        """Сохраняет настройки в config.json."""
        data = {
            "chat_id": self.chat_id_input.text(),
            "user_data_dir": self.user_data_dir_input.text(),
            "quotes_path": self.quotes_path_input.text(),
            "message_count": self.message_count_input.value(),
            "interval": self.interval_input.value(),
            "profile": self.profile_combo.currentText(),
            "remember": self.save_settings_checkbox.isChecked(),
            "auto_launch": self.auto_launch_checkbox.isChecked(),
            "day_of_week": self.day_of_week_combo.currentText(),
            "time": self.time_edit.time().toString("HH:mm"),
            "next_launch": self.next_launch.isoformat() if self.next_launch else ""
        }
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")

    def check_and_run_script(self):
        now = datetime.datetime.now()
        if self.next_launch and now >= self.next_launch:
            log_entry = self.read_log_entry(self.next_launch)
            if not log_entry and self.auto_launch_checkbox.isChecked():
                self.start_sending_messages(automatic=True)

    def read_log_entry(self, selected_datetime):
        if not os.path.exists(LOG_FILE):
            return False

        with open(LOG_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in reversed(lines):
                if selected_datetime.strftime("%Y-%m-%d %A %H:%M") in line:
                    return True
        return False

    def log_script_execution(self):
        now = datetime.datetime.now()
        log_message = f"{now.strftime('%Y-%m-%d %A %H:%M')} - Сообщения отправлены. ID чата: {self.chat_id_input.text()}, Количество сообщений: {self.message_count_input.value()}\n"

    # Читаем текущий лог
        try:
            with open(LOG_FILE, "r+", encoding="utf-8") as file:
                lines = file.readlines()
                if len(lines) >= 5:  # Ограничиваем лог до 5 записей
                    file.seek(0)
                    file.truncate()  # Очищаем файл перед записью новых данных
                    file.write(log_message)
                else:
                    file.write(log_message)
        except FileNotFoundError:
            # Если файл не существует, создаем его и записываем первую строку
            with open(LOG_FILE, "w", encoding="utf-8") as file:
                file.write(log_message)

        # Обновляем дату и время следующего автозапуска
        self.update_next_launch()

    def update_next_launch(self):
        now = datetime.datetime.now()
        selected_day_of_week = self.day_of_week_combo.currentText()
        selected_time = self.time_edit.time().toPython()
        selected_datetime = datetime.datetime(now.year, now.month, now.day, selected_time.hour, selected_time.minute)

        # Преобразуем выбранный день недели в номер дня недели (0 - понедельник, 6 - воскресенье)
        day_map = {
            "Понедельник": 0,
            "Вторник": 1,
            "Среда": 2,
            "Четверг": 3,
            "Пятница": 4,
            "Суббота": 5,
            "Воскресенье": 6
        }
        selected_day_number = day_map[selected_day_of_week]

        # Вычисляем разницу между текущим днем недели и выбранным
        days_until_next_launch = (selected_day_number - now.weekday()) % 7
        if days_until_next_launch == 0 and selected_datetime <= now:
            days_until_next_launch = 7  # Если день совпадает, но время уже прошло, добавляем неделю

        self.next_launch = selected_datetime + datetime.timedelta(days=days_until_next_launch)

    def on_day_or_time_changed(self):
        """Обновляет конфигурацию при изменении дня недели или времени."""
        self.save_settings()
        self.update_next_launch()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.day_of_week_combo.currentIndexChanged.connect(window.on_day_or_time_changed)
    window.time_edit.timeChanged.connect(window.on_day_or_time_changed)
    window.show()
    sys.exit(app.exec())