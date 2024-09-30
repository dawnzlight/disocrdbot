import json
import os
from abc import ABCMeta, abstractmethod


class Config(metaclass=ABCMeta):

    def __init__(self, env):
        self.env = env

    @abstractmethod
    def get_discord_bot_token(self):        
        raise NotImplementedError()
    

class DevelopmentConfig(Config):
    
    def __init__(self):
        super().__init__('development')
        
        with open('secrets.json') as f:
            data = json.load(f)

        self.data = data['development']

    def get_discord_bot_token(self):
        return self.data['discord_bot_token']
    
    def get_text_channels(self):
        return self.data['text_channel_id']
    
    def get_text_channel(self, name):
        return self.data['text_channel_id'][name]
    

class ProductionConfig(Config):

    def __init__(self):
        super().__init__('production')
        self.data = {
            'discord_bot_token': os.environ['BOT_TOKEN'],
            'text_channel_id': {
                'notification': os.environ['VOICE_CHAT_TEXT']
            }
        }

    def get_discord_bot_token(self):
        return self.data['discord_bot_token']
    
    def get_text_channels(self):
        return self.data['text_channel_id']
    
    def get_text_channel(self, name):
        return self.data['text_channel_id'][name]
        

