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
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QCheckBox, QSpinBox
)
from PySide6.QtCore import QThread, Signal, Qt, QSize
from styles import *
from script import send_messages

# Путь к файлу конфигурации
CONFIG_FILE = "config.json"

# Основной класс для работы с VK Messenger
class VKMessengerWorker(QThread):
    finished = Signal(str)  # Сигнал для уведомления об окончании работы

    def __init__(self, chat_id, user_data_dir, quotes_path, message_count, interval):
        super().__init__()
        self.chat_id = chat_id
        self.user_data_dir = user_data_dir
        self.quotes_path = quotes_path
        self.message_count = message_count
        self.interval = interval

    def run(self):
        try:
            from script import send_messages
            send_messages(
                self.chat_id,
                self.user_data_dir,
                self.quotes_path,
                self.message_count,
                self.interval
            )
            self.finished.emit("Все сообщения отправлены успешно!")
        except Exception as e:
            self.finished.emit(f"Ошибка: {str(e)}")

# Главное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Настройка главного окна
        self.setWindowTitle("VK Messenger Bot")
        self.setGeometry(200, 200, 600, 450)
        self.setWindowIcon(QIcon("icons/icon.png"))  # Добавьте иконку для приложения

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Вертикальный макет
        layout = QVBoxLayout()

        # Заголовок
        title_label = QLabel("VK Messenger Bot")
        title_label.setFont(QFont("Roboto", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(get_title_style())
        layout.addWidget(title_label)

        # ID чата
        chat_id_layout = QHBoxLayout()
        self.chat_id_label = QLabel("ID чата:")
        self.chat_id_label.setFont(QFont("Roboto", 14))
        self.chat_id_label.setStyleSheet(get_label_style())
        chat_id_layout.addWidget(self.chat_id_label)

        self.chat_id_input = QLineEdit()
        self.chat_id_input.setText(self.load_config().get("chat_id", ""))
        self.chat_id_input.setPlaceholderText("Введите или вставьте ID чата")
        self.chat_id_input.setFont(QFont("Roboto", 14))
        self.chat_id_input.setStyleSheet(get_input_style())
        chat_id_layout.addWidget(self.chat_id_input)
        layout.addLayout(chat_id_layout)

        # Путь к папке профиля Chrome
        user_data_layout = QHBoxLayout()
        self.user_data_dir_label = QLabel("Путь к папке профиля Chrome:")
        self.user_data_dir_label.setFont(QFont("Roboto", 14))
        self.user_data_dir_label.setStyleSheet(get_label_style())
        user_data_layout.addWidget(self.user_data_dir_label)

        self.user_data_dir_input = QLineEdit()
        self.user_data_dir_input.setText(self.load_config().get("user_data_dir", ""))
        self.user_data_dir_input.setPlaceholderText("Например, C:\\Users\\<имя_пользователя>\\AppData\\Local\\Google\\Chrome\\User Data")
        self.user_data_dir_input.setFont(QFont("Roboto", 14))
        self.user_data_dir_input.setStyleSheet(get_input_style())
        user_data_layout.addWidget(self.user_data_dir_input)

        self.user_data_dir_button = QPushButton("Выбрать папку")
        self.user_data_dir_button.setFont(QFont("Roboto", 14, QFont.Bold))
        self.user_data_dir_button.setIcon(QIcon("icons/folder_icon_128.png"))
        self.user_data_dir_button.setIconSize(QSize(32, 32))
        self.user_data_dir_button.setStyleSheet(get_button_style())
        self.user_data_dir_button.clicked.connect(self.select_user_data_dir)
        user_data_layout.addWidget(self.user_data_dir_button)
        layout.addLayout(user_data_layout)

        # Файл с цитатами
        quotes_layout = QHBoxLayout()
        self.quotes_label = QLabel("Файл с цитатами:")
        self.quotes_label.setFont(QFont("Roboto", 14))
        self.quotes_label.setStyleSheet(get_label_style())
        quotes_layout.addWidget(self.quotes_label)

        self.quotes_input = QLineEdit()
        self.quotes_input.setText(self.load_config().get("quotes_path", ""))
        self.quotes_input.setPlaceholderText("Выберите файл с цитатами")
        self.quotes_input.setFont(QFont("Roboto", 14))
        self.quotes_input.setStyleSheet(get_input_style())
        quotes_layout.addWidget(self.quotes_input)

        self.quotes_button = QPushButton("Выбрать файл")
        self.quotes_button.setFont(QFont("Roboto", 14, QFont.Bold))
        self.quotes_button.setIcon(QIcon("icons/file_icon_128.png"))
        self.quotes_button.setIconSize(QSize(32, 32))
        self.quotes_button.setStyleSheet(get_button_style())
        self.quotes_button.clicked.connect(self.select_quotes_file)
        quotes_layout.addWidget(self.quotes_button)
        layout.addLayout(quotes_layout)

        # Количество сообщений
        message_count_layout = QHBoxLayout()
        self.message_count_label = QLabel("Количество сообщений:")
        self.message_count_label.setFont(QFont("Roboto", 14))
        self.message_count_label.setStyleSheet(get_label_style())
        message_count_layout.addWidget(self.message_count_label)

        self.message_count_input = QSpinBox()
        self.message_count_input.setValue(self.load_config().get("message_count", 10))
        self.message_count_input.setFont(QFont("Roboto", 14))
        self.message_count_input.setStyleSheet(get_input_style())
        message_count_layout.addWidget(self.message_count_input)
        layout.addLayout(message_count_layout)

        # Интервал отправки
        interval_layout = QHBoxLayout()
        self.interval_label = QLabel("Интервал отправки (сек):")
        self.interval_label.setFont(QFont("Roboto", 14))
        self.interval_label.setStyleSheet(get_label_style())
        interval_layout.addWidget(self.interval_label)

        self.interval_input = QSpinBox()
        self.interval_input.setValue(self.load_config().get("interval", 3))
        self.interval_input.setFont(QFont("Roboto", 14))
        self.interval_input.setStyleSheet(get_input_style())
        interval_layout.addWidget(self.interval_input)
        layout.addLayout(interval_layout)

        # Галочка "Запомнить"
        self.remember_checkbox = QCheckBox("Запомнить данные")
        self.remember_checkbox.setFont(QFont("Roboto", 14))
        self.remember_checkbox.setStyleSheet(get_checkbox_style())
        self.remember_checkbox.setChecked(self.load_config().get("remember", False))
        layout.addWidget(self.remember_checkbox)

        # Кнопки управления
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Запустить скрипт")
        self.start_button.setFont(QFont("Roboto", 16, QFont.Bold))
        self.start_button.setIcon(QIcon("icons/play_icon_128.png"))
        self.start_button.setIconSize(QSize(64, 64))
        self.start_button.setStyleSheet(get_start_script_button_style())
        self.start_button.clicked.connect(self.start_script)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Выход")
        self.stop_button.setFont(QFont("Roboto", 16, QFont.Bold))
        self.stop_button.setIcon(QIcon("icons/exit_icon_128.png"))
        self.stop_button.setIconSize(QSize(64, 64))
        self.stop_button.setStyleSheet(get_button_style())
        self.stop_button.clicked.connect(self.close)
        button_layout.addWidget(self.stop_button)
        layout.addLayout(button_layout)

        # Добавляем информацию об авторе приложения
        author_label = QLabel("Автор приложения: Сергей Каманов")
        author_label.setFont(QFont("Roboto", 12))
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setStyleSheet(get_author_label_style())
        layout.addWidget(author_label)

        # Устанавливаем макет
        central_widget.setLayout(layout)

        # Поток для выполнения скрипта
        self.worker_thread = None

    # Загрузка данных из файла конфигурации
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    # Сохранение данных в файл конфигурации
    def save_config(self, data):
        if self.remember_checkbox.isChecked():
            with open(CONFIG_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        elif os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)

    # Выбор пути к папке профиля Chrome
    def select_user_data_dir(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку профиля Chrome")
        if folder_path:
            self.user_data_dir_input.setText(folder_path)

    # Выбор файла с цитатами
    def select_quotes_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл с цитатами", "", "Текстовые файлы (*.txt)")
        if file_path:
            self.quotes_input.setText(file_path)

    # Запуск скрипта
    def start_script(self):
        chat_id = self.chat_id_input.text().strip()
        user_data_dir = self.user_data_dir_input.text().strip()
        quotes_path = self.quotes_input.text().strip()
        message_count = self.message_count_input.value()
        interval = self.interval_input.value()

        if not chat_id:
            QMessageBox.critical(self, "Ошибка", "Введите ID чата!")
            return
        if not user_data_dir:
            QMessageBox.critical(self, "Ошибка", "Укажите путь к папке профиля Chrome!")
            return
        if not os.path.exists(quotes_path):
            QMessageBox.critical(self, "Ошибка", "Файл с цитатами не найден!")
            return

        config_data = {
            "chat_id": chat_id,
            "user_data_dir": user_data_dir,
            "quotes_path": quotes_path,
            "remember": self.remember_checkbox.isChecked(),
            "message_count": message_count,
            "interval": interval
        }
        self.save_config(config_data)

        self.worker_thread = VKMessengerWorker(chat_id, user_data_dir, quotes_path, message_count, interval)
        self.worker_thread.finished.connect(self.on_script_finished)
        self.worker_thread.start()

        self.start_button.setEnabled(False)

    # Обработка завершения работы скрипта
    def on_script_finished(self, message):
        QMessageBox.information(self, "Скрипт завершен", message)
        self.start_button.setEnabled(True)

# Точка входа в приложение
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Настройка глобального стиля
    app.setStyleSheet(get_global_style())

    # Создание главного окна
    window = MainWindow()
    window.show()

    # Запуск приложения
    sys.exit(app.exec())