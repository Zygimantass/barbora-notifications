import telegram
from notifier import Notifier

class TelegramNotifier(Notifier):
    def __init__(self, token, group_id):
        self.bot = telegram.Bot(token=token)
        self.group_id = group_id

    def notify(self, message):
        self.bot.send_message(self.group_id, message)
