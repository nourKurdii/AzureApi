import base64
from dataclasses import dataclass
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")


@dataclass(frozen=True)
class Configurations:
    """ immutable dataclass to store the immutable configurations"""

    pat: str = str(config['pat_info']['pat'])
    organization: str = str(config['organization_info']['organization'])
    # encrypt the pat using base64 encryption
    authorization: str = str(base64.b64encode(bytes(':' + pat, 'ascii')), 'ascii')
    KEY = str(config['Telegram_bot_info']['key'])
    CHANNEL = str(config['Telegram_bot_info']['channel_id'])
