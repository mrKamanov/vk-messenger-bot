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
        self.automatic = False

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