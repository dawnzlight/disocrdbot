import requests


class Gemini:

    def __init__(self, config):
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.api_key = config.get_gemini_api_key()
        self.url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest'
        self.config = config

    def generate_content(self, prompt):
        data = {
            'contents': [{'parts':[{"text":self.config.get_prompt(prompt)}]}]
        }
        return requests.post(f"{self.url}:generateContent?key={self.api_key}", headers=self.headers, json=data).json()