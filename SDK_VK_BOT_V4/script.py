# Copyright <2025> <Сергей Каманов>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # Импорт Keys
from selenium.common.exceptions import TimeoutException  # Импорт TimeoutException
import time
import logging
import random

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_quotes(quotes_path):
    """
    Загружает цитаты из указанного файла.
    :param quotes_path: Путь к файлу с цитатами.
    :return: Список строк с цитатами.
    """
    with open(quotes_path, 'r', encoding='utf-8') as file:
        quotes = [line.strip() for line in file if line.strip()]
        if not quotes:
            raise ValueError("Файл с цитатами пуст или не содержит валидных строк.")
        return quotes

def send_messages(chat_id, user_data_dir, quotes_path, message_count=10, interval=3, profile="Default"):
    """
    Отправляет сообщения в указанный чат VK Messenger.
    :param chat_id: ID чата.
    :param user_data_dir: Путь к папке профиля Chrome.
    :param quotes_path: Путь к файлу с цитатами.
    :param message_count: Количество сообщений для отправки (по умолчанию 10).
    :param interval: Интервал между отправкой сообщений в секундах (по умолчанию 3).
    :param profile: Имя профиля Chrome (например, "Default" или "Profile 1").
    """
    options = Options()
    options.add_argument(f"user-data-dir={user_data_dir}")
    options.add_argument(f"--profile-directory={profile}")
    options.add_argument("--start-maximized")
    driver = None
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        logging.info("Браузер запущен.")
        driver.get(f'https://web.vk.me/convo/{chat_id}?entrypoint=list_all')
        logging.info("Чат открыт успешно!")
        # Проверка на наличие капчи
        captcha_element = driver.find_elements(By.XPATH, "//div[contains(@class, 'captcha')]")
        if captcha_element:
            logging.warning("Обнаружена капча. Пожалуйста, решите её вручную.")
            input("Нажмите Enter после решения капчи...")
        # Нахождение поля ввода сообщения
        message_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@aria-label='Напишите сообщение...']"))
        )
        # Загрузка цитат
        quotes = load_quotes(quotes_path)
        # Отправка сообщений
        for i in range(min(message_count, len(quotes))):
            quote = quotes[i]
            message_input.send_keys(quote)
            message_input.send_keys(Keys.RETURN)  # Использование Keys.RETURN
            logging.info(f"Сообщение '{quote}' отправлено!")
            # Ожидание перед отправкой следующего сообщения
            wait_time = random.uniform(interval - 1, interval + 1)
            time.sleep(wait_time)
            logging.info(f"Ожидаю {wait_time:.2f} секунд перед следующим сообщением.")
        logging.info("Все сообщения отправлены успешно!")
    except FileNotFoundError as e:
        logging.error(f"Файл с цитатами не найден: {e}")
    except TimeoutException as e:  # Использование TimeoutException
        logging.error(f"Превышено время ожидания элемента: {e}")
    except Exception as e:
        logging.error(f"Неизвестная ошибка: {e}")
    finally:
        if driver:
            try:
                driver.quit()
                logging.info("Браузер закрыт.")
            except Exception as e:
                logging.warning(f"Ошибка при закрытии WebDriver: {e}")