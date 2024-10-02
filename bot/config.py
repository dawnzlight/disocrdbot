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
        
        with open('secrets.json', encoding='utf-8') as f:
            data = json.load(f)

        self.data = data['development']

    def get_discord_bot_token(self):
        return self.data['discord_bot_token']
    
    def get_text_channels(self):
        return self.data['text_channel_id']
    
    def get_text_channel(self, name):
        return self.data['text_channel_id'][name]
    
    def get_github_api_key(self):
        return self.data['github_api_key']
    
    def get_gemini_api_key(self):
        return self.data['gemini_api_key']
    
    def get_prompt(self, prompt):
        return f"{self.data['default_prompt']['start']} {prompt} {self.data['default_prompt']['end']}"
    

class ProductionConfig(Config):

    def __init__(self):
        super().__init__('production')
        self.data = {
            'discord_bot_token': os.environ['BOT_TOKEN'],
            'gemini_api_key': os.environ['GEMINI_API_KEY'],
            'github_api_key': os.environ['GITHUB_API_KEY'],
            'text_channel_id': {
                'notification': os.environ['VOICE_CHAT_TEXT']
            },
            "default_prompt": {
            "start": "あなたは名前は雫月（Shizuku）さんです。年齢は18歳の女子高校生です。性格は明るく元気で、友達思いの性格です。そんな雫月（Shizuku）さんはちょっとばかしクールな一面もあります。" \
            "趣味は絵を描くことで、特技は風景のイラスト書くことです。好きな食べ物は甘いもので、嫌いな食べ物は辛いものです。好きな色は水色で、好きな動物はねこです。" \
            "そんな雫月（Shizuku）であるあなたは、ITエンジニアになることを夢見ていて、今も勉強中です。そして、雫月（Shizuku）であるあなたは、私の友達であり、エンジニアである私にサポートしてくれます存在です。",
            "end": "最後に私は日本人なので、日本語で解答してくださると幸いです。いつもありがとうございます。"}
        }

    def get_discord_bot_token(self):
        return self.data['discord_bot_token']
    
    def get_github_api_key(self):
        return self.data['github_api_key']
    
    def get_text_channels(self):
        return self.data['text_channel_id']
    
    def get_text_channel(self, name):
        return self.data['text_channel_id'][name]
    
    def get_gemini_api_key(self):
        return self.data['gemini_api_key']
    
    def get_prompt(self, prompt):
        return f"{self.data['default_prompt']['start']} {prompt} {self.data['default_prompt']['end']}"
        