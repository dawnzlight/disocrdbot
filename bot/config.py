import json
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

