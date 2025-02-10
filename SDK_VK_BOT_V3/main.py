# Copyright <2025> <Сергей Каманов>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLineEdit, QLabel,
    QComboBox, QSpinBox, QCheckBox, QVBoxLayout, QWidget, QFileDialog, QProgressBar
)
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QIcon  # Импортируем QIcon
from VKMessengerWorker import VKMessengerWorker
from themes import get_global_style, get_title_style, get_input_style, get_checkbox_style, get_author_label_style

CONFIG_PATH = "config.json"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Устанавливаем иконку приложения
        app_icon_path = "icons/icon.ico"
        if os.path.exists(app_icon_path):
            self.setWindowIcon(QIcon(app_icon_path))
        else:
            print(f"Иконка приложения не найдена: {app_icon_path}")

        # Интерфейс
        self.setWindowTitle("VK Messenger Automation")
        self.setStyleSheet(get_global_style())
        self.setGeometry(100, 100, 800, 600)  # Изменено соотношение сторон на 4:3
        # Центральный виджет
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        # Layout
        layout = QVBoxLayout(central_widget)
        # Заголовок
        self.title_label = QLabel("VK Messenger Automation", self)
        self.title_label.setStyleSheet(get_title_style())
        layout.addWidget(self.title_label)

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
        folder_icon_path = "icons/folder_icon.png"
        if os.path.exists(folder_icon_path):
            self.user_data_dir_button.setIcon(QIcon(folder_icon_path))
        else:
            print(f"Иконка не найдена: {folder_icon_path}")
        self.user_data_dir_button.setIconSize(QSize(24, 24))  # Размер иконки
        self.user_data_dir_button.clicked.connect(self.select_user_data_dir)
        layout.addWidget(self.user_data_dir_button)

        self.quotes_path_input = QLineEdit(self)
        self.quotes_path_input.setPlaceholderText("Выберите файл с цитатами")
        self.quotes_path_input.setStyleSheet(get_input_style())
        layout.addWidget(self.quotes_path_input)

        # Кнопка выбора файла с цитатами
        self.quotes_path_button = QPushButton("Выбрать файл", self)
        file_icon_path = "icons/file_icon.png"
        if os.path.exists(file_icon_path):
            self.quotes_path_button.setIcon(QIcon(file_icon_path))
        else:
            print(f"Иконка не найдена: {file_icon_path}")
        self.quotes_path_button.setIconSize(QSize(24, 24))  # Размер иконки
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

        # Кнопка обновления списка профилей
        self.update_profiles_button = QPushButton("Обновить профили", self)
        profile_icon_path = "icons/profile_icon.png"
        if os.path.exists(profile_icon_path):
            self.update_profiles_button.setIcon(QIcon(profile_icon_path))
        else:
            print(f"Иконка не найдена: {profile_icon_path}")
        self.update_profiles_button.setIconSize(QSize(24, 24))  # Размер иконки
        self.update_profiles_button.clicked.connect(self.update_profile_list)
        layout.addWidget(self.update_profiles_button)

        # Выпадающий список профилей
        self.profile_combo = QComboBox(self)
        self.profile_combo.addItems(["Default"])  # Начальный профиль
        self.profile_combo.setStyleSheet(get_input_style())
        layout.addWidget(self.profile_combo)

        self.save_settings_checkbox = QCheckBox("Запомнить настройки", self)
        self.save_settings_checkbox.setStyleSheet(get_checkbox_style())
        layout.addWidget(self.save_settings_checkbox)

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

        # Кнопка "Отправить сообщения"
        self.send_button = QPushButton("Отправить сообщения", self)
        play_icon_path = "icons/play_icon.png"
        if os.path.exists(play_icon_path):
            self.send_button.setIcon(QIcon(play_icon_path))
        else:
            print(f"Иконка не найдена: {play_icon_path}")
        self.send_button.setIconSize(QSize(24, 24))  # Размер иконки
        self.send_button.clicked.connect(self.start_sending_messages)
        layout.addWidget(self.send_button)

        # Кнопка "Выход"
        self.exit_button = QPushButton("Выход", self)
        exit_icon_path = "icons/exit_icon.png"
        if os.path.exists(exit_icon_path):
            self.exit_button.setIcon(QIcon(exit_icon_path))
        else:
            print(f"Иконка не найдена: {exit_icon_path}")
        self.exit_button.setIconSize(QSize(24, 24))  # Размер иконки
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        # Статус-лейбл
        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet("color: #D1D5DB; font-family: 'Poppins', sans-serif; font-size: 14px;")
        layout.addWidget(self.status_label)

        # Авторский текст
        self.author_label = QLabel("Автор приложения: Сергей Каманов", self)
        self.author_label.setStyleSheet(get_author_label_style())
        layout.addWidget(self.author_label)

        # Загружаем настройки
        self.load_settings()

    def select_user_data_dir(self):
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку профиля Chrome")
        if folder:
            self.user_data_dir_input.setText(folder)

    def select_quotes_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл с цитатами", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.quotes_path_input.setText(file_path)

    def start_sending_messages(self):
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
        self.send_button.setDisabled(True)  # Блокировка кнопки
        self.send_button.setText("Отправка...")  # Изменяем текст кнопки

        self.status_label.setText("Отправка сообщений...")
        self.worker = VKMessengerWorker(chat_id, user_data_dir, quotes_path, message_count, interval, profile)
        self.worker.finished.connect(self.update_status)  # Подключаем обработчик завершения
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
        self.send_button.setEnabled(True)  # Разблокировка кнопки
        self.send_button.setText("Отправить сообщения")  # Возвращаем исходный текст

    def update_profile_list(self):
        """ Обновляет список профилей в выпадающем меню """
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
        """ Загружает настройки из config.json """
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
            except Exception as e:
                print(f"Ошибка загрузки конфигурации: {e}")

    def save_settings(self):
        """ Сохраняет настройки в config.json """
        data = {
            "chat_id": self.chat_id_input.text(),
            "user_data_dir": self.user_data_dir_input.text(),
            "quotes_path": self.quotes_path_input.text(),
            "message_count": self.message_count_input.value(),
            "interval": self.interval_input.value(),
            "profile": self.profile_combo.currentText(),
            "remember": self.save_settings_checkbox.isChecked()
        }
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())