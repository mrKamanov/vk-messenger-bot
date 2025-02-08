# Copyright <2025> <Сергей Каманов>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Функция для чтения цитат из файла
def load_quotes(quotes_path):
    """
    Загружает цитаты из указанного файла.

    :param quotes_path: Путь к файлу с цитатами.
    :return: Список строк с цитатами.
    """
    with open(quotes_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]


# Основная функция для отправки сообщений
def send_messages(chat_id, user_data_dir, quotes_path, message_count=10, interval=3):
    """
    Отправляет сообщения в указанный чат VK Messenger.

    :param chat_id: ID чата.
    :param user_data_dir: Путь к папке профиля Chrome.
    :param quotes_path: Путь к файлу с цитатами.
    :param message_count: Количество сообщений для отправки (по умолчанию 10).
    :param interval: Интервал между отправкой сообщений в секундах (по умолчанию 3).
    """
    # Настройка WebDriver
    options = Options()
    options.add_argument(f"user-data-dir={user_data_dir}")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        # Открываем чат
        driver.get(f'https://web.vk.me/convo/{chat_id}?entrypoint=list_all')
        print("Чат открыт успешно!")

        # Нахождение поля ввода сообщения
        message_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@aria-label='Напишите сообщение...']"))
        )

        # Загрузка цитат
        quotes = load_quotes(quotes_path)

        # Отправка указанного количества сообщений с заданным интервалом
        for i in range(min(message_count, len(quotes))):
            quote = quotes[i]
            message_input.send_keys(quote)
            print(f"Сообщение '{quote}' отправлено!")
            message_input.send_keys(Keys.RETURN)
            time.sleep(interval)  # Используем переданный интервал между сообщениями

        print("Все сообщения отправлены успешно!")

    except Exception as e:
        print("Ошибка при отправке сообщений:", e)

    finally:
        # Закрываем браузер после завершения работы
        driver.quit() 
