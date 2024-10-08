import requests


class Gemini:

    def __init__(self, config):
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.api_key = config.get_gemini_api_key()
        self.url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest'
        self.config = config

    def generate_content(self, prompt, category=''):
        
        if category == 'question':
            text = 'ここであなたに私はこんな質問をします。'
            data = {
                'contents': [{'parts':[{"text":self.config.get_prompt(f'{text} {prompt}')}]}]
            }
            return requests.post(f"{self.url}:generateContent?key={self.api_key}", headers=self.headers, json=data).json()
        elif category == 'comment':
            text = 'ここであなたは次の文章に関してコメントをしてください。'
            data = {
                'contents': [{'parts':[{"text":self.config.get_prompt(f'{text} {prompt}')}]}]
            }
            return requests.post(f"{self.url}:generateContent?key={self.api_key}", headers=self.headers, json=data).json()
        elif category == 'default':
            data = {
                'contents': [{'parts':[{"text":prompt}]}]
            }
            return requests.post(f"{self.url}:generateContent?key={self.api_key}", headers=self.headers, json=data).json()
        else:
            data = {
                'contents': [{'parts':[{"text":self.config.get_prompt(prompt)}]}]
            }
            return requests.post(f"{self.url}:generateContent?key={self.api_key}", headers=self.headers, json=data).json()
        