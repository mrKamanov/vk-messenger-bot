# Copyright <2025> <Сергей Каманов>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from PySide6.QtCore import QThread, Signal
from script import send_messages

class VKMessengerWorker(QThread):
    finished = Signal(str)

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
