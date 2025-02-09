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
    QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox, QCheckBox, QSpinBox, QComboBox
)
from PySide6.QtCore import QThread, Signal, Qt, QSize
from styles import (
    get_global_style, get_input_style,
    get_title_style, get_label_style, get_author_label_style, get_checkbox_style
)

CONFIG_FILE = "config.json"

class VKMessengerWorker(QThread):
    finished = Signal(str)  # Сигнал для уведомления об окончании работы

    def __init__(self, chat_id, user_data_dir, quotes_path, message_count, interval, profile):
        super().__init__()
        self.chat_id = chat_id
        self.user_data_dir = user_data_dir
        self.quotes_path = quotes_path
        self.message_count = message_count
        self.interval = interval
        self.profile = profile

    def run(self):
        try:
            from script import send_messages
            send_messages(
                self.chat_id,
                self.user_data_dir,
                self.quotes_path,
                self.message_count,
                self.interval,
                self.profile
            )
            self.finished.emit("Все сообщения отправлены успешно!")
        except Exception as e:
            self.finished.emit(f"Ошибка: {str(e)}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VK Messenger Bot")
        self.setGeometry(200, 200, 600, 450)
        self.setWindowIcon(QIcon("icons/icon.png"))  # Добавьте иконку для приложения

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        title_label = QLabel("VK Messenger Bot")
        title_label.setFont(QFont("Roboto", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(get_title_style())
        layout.addWidget(title_label)

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

        user_data_layout = QHBoxLayout()
        self.user_data_dir_label = QLabel("Путь к папке профиля Chrome:")
        self.user_data_dir_label.setFont(QFont("Roboto", 14))
        self.user_data_dir_label.setStyleSheet(get_label_style())
        user_data_layout.addWidget(self.user_data_dir_label)

        self.user_data_dir_input = QLineEdit()
        self.user_data_dir_input.setText(self.load_config().get("user_data_dir", ""))
        self.user_data_dir_input.setPlaceholderText(
            "Например, C:\\Users\\<имя_пользователя>\\AppData\\Local\\Google\\Chrome\\User Data"
        )
        self.user_data_dir_input.setFont(QFont("Roboto", 14))
        self.user_data_dir_input.setStyleSheet(get_input_style())
        user_data_layout.addWidget(self.user_data_dir_input)

        self.user_data_dir_button = QPushButton("Выбрать папку")
        self.user_data_dir_button.setFont(QFont("Roboto", 14, QFont.Bold))
        self.user_data_dir_button.setIcon(QIcon("icons/folder_icon.png"))
        self.user_data_dir_button.setIconSize(QSize(32, 32))
        self.user_data_dir_button.setStyleSheet(get_input_style())  # Используем стиль
        self.user_data_dir_button.clicked.connect(self.select_user_data_dir)
        user_data_layout.addWidget(self.user_data_dir_button)

        layout.addLayout(user_data_layout)

        profile_layout = QHBoxLayout()
        self.profile_label = QLabel("Выберите профиль:")
        self.profile_label.setFont(QFont("Roboto", 14))
        self.profile_label.setStyleSheet(get_label_style())
        profile_layout.addWidget(self.profile_label)

        self.profile_combobox = QComboBox()
        self.profile_combobox.setFont(QFont("Roboto", 14))
        self.profile_combobox.setStyleSheet(get_input_style())
        self.profile_combobox.setVisible(False)  # Скрываем до выбора папки
        profile_layout.addWidget(self.profile_combobox)

        self.update_profiles_button = QPushButton("Обновить профили")
        self.update_profiles_button.setFont(QFont("Roboto", 14, QFont.Bold))
        self.update_profiles_button.setIcon(QIcon("icons/profile_icon.png"))
        self.update_profiles_button.setIconSize(QSize(32, 32))
        self.update_profiles_button.setStyleSheet(get_input_style())  # Используем стиль
        self.update_profiles_button.clicked.connect(self.load_profiles)
        profile_layout.addWidget(self.update_profiles_button)

        layout.addLayout(profile_layout)

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
        self.quotes_button.setIcon(QIcon("icons/file_icon.png"))
        self.quotes_button.setIconSize(QSize(32, 32))
        self.quotes_button.setStyleSheet(get_input_style())  # Используем стиль
        self.quotes_button.clicked.connect(self.select_quotes_file)
        quotes_layout.addWidget(self.quotes_button)

        layout.addLayout(quotes_layout)

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

        self.remember_checkbox = QCheckBox("Запомнить данные")
        self.remember_checkbox.setFont(QFont("Roboto", 14))
        self.remember_checkbox.setStyleSheet(get_checkbox_style())
        self.remember_checkbox.setChecked(self.load_config().get("remember", False))
        layout.addWidget(self.remember_checkbox)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Запустить скрипт")
        self.start_button.setFont(QFont("Roboto", 16, QFont.Bold))
        self.start_button.setIcon(QIcon("icons/play_icon.png"))
        self.start_button.setIconSize(QSize(64, 64))
        self.start_button.setStyleSheet(get_input_style())  # Используем стиль
        self.start_button.clicked.connect(self.start_script)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Выход")
        self.stop_button.setFont(QFont("Roboto", 16, QFont.Bold))
        self.stop_button.setIcon(QIcon("icons/exit_icon.png"))
        self.stop_button.setIconSize(QSize(64, 64))
        self.stop_button.setStyleSheet(get_input_style())  # Используем стиль
        self.stop_button.clicked.connect(self.close)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

        author_label = QLabel("Автор приложения: Сергей Каманов")
        author_label.setFont(QFont("Roboto", 12))
        author_label.setAlignment(Qt.AlignCenter)
        author_label.setStyleSheet(get_author_label_style())
        layout.addWidget(author_label)

        central_widget.setLayout(layout)

        self.worker_thread = None

        user_data_dir = self.load_config().get("user_data_dir")
        if user_data_dir:
            self.user_data_dir_input.setText(user_data_dir)
            self.load_profiles()  # Автоматически загружаем профили

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return {}

    def save_config(self, data):
        if self.remember_checkbox.isChecked():
            with open(CONFIG_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        elif os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)

    def select_user_data_dir(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку профиля Chrome")
        if folder_path:
            self.user_data_dir_input.setText(folder_path)
            self.load_profiles()  # Обновляем профили после выбора папки

    def load_profiles(self):
        user_data_dir = self.user_data_dir_input.text().strip()
        if not os.path.exists(user_data_dir):
            QMessageBox.critical(self, "Ошибка", "Указанная папка не существует!")
            return

        profiles = []
        for folder in os.listdir(user_data_dir):
            folder_path = os.path.join(user_data_dir, folder)
            if os.path.isdir(folder_path) and folder.startswith(("Default", "Profile")):
                profiles.append(folder)

        if not profiles:
            QMessageBox.warning(self, "Внимание", "Профили не найдены!")
            return

        self.profile_combobox.clear()
        self.profile_combobox.addItems(profiles)
        self.profile_combobox.setVisible(True)

    def select_quotes_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл с цитатами", "", "Текстовые файлы (*.txt)")
        if file_path:
            self.quotes_input.setText(file_path)

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

        selected_profile = self.profile_combobox.currentText()
        if not selected_profile:
            QMessageBox.critical(self, "Ошибка", "Выберите профиль Chrome!")
            return

        config_data = {
            "chat_id": chat_id,
            "user_data_dir": user_data_dir,
            "quotes_path": quotes_path,
            "remember": self.remember_checkbox.isChecked(),
            "message_count": message_count,
            "interval": interval,
            "selected_profile": selected_profile
        }
        self.save_config(config_data)

        self.worker_thread = VKMessengerWorker(
            chat_id=chat_id,
            user_data_dir=user_data_dir,
            quotes_path=quotes_path,
            message_count=message_count,
            interval=interval,
            profile=selected_profile
        )
        self.worker_thread.finished.connect(self.on_script_finished)
        self.worker_thread.start()
        self.start_button.setEnabled(False)

    def on_script_finished(self, message):
        QMessageBox.information(self, "Скрипт завершен", message)
        self.start_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(get_global_style())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())