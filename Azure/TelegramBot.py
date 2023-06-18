import httpx
from ConfigurationsDataClass import Configurations


class TelegramBot:
    """class for Telegram bot"""
    def __init__(self):
        self.sett = Configurations()
        self.base_url = None

    def add_msg(self, msg):
        """append  the msg to the url"""
        self.base_url = f'https://api.telegram.org/bot{self.sett.KEY}' \
                        f'/sendMessage?chat_id={self.sett.CHANNEL}&text={msg}'

    def get_base_url(self):
        """getter for base url"""
        return self.base_url

    def send_msg(self):
        """send the msg to the telegram bot"""
        httpx.get(url=self.get_base_url())
