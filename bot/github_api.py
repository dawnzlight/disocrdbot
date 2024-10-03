import json

import requests


class Github:

    def __init__(self, config):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {config.get_github_api_key()}',
            'X-GitHub-Api-Version': '2022-11-28',
        }
        self.api_key = config.get_github_api_key()
        self.config = config
        self.url = 'https://api.github.com'
        self.owner = 'dawnzlight'
        self.discord_member_id = {
            'CoCo9122': '691214730643374080',
            'Maneo9910': '691094528349831259'
        }
        self.reviewer = ['CoCo9122', 'Maneo9910']

    def get_disocrd_member_id(self, member):
        if member in self.discord_member_id:
            return self.discord_member_id[member]
        else:
            return member

    def get_pull_requests(self, repo):

        headers = self.headers
        headers['Accept'] = 'application/vnd.github.v3+json'

        responses = requests.get(f"{self.url}/repos/{self.owner}/{repo}/pulls", headers=headers).json()

        pull_requests = [ {
            'url': response['url'],
            'html_url': response['html_url'],
            'title': response['title'],
            'number': response['number'],
            'user':response['user']['login'],
            "created_at": response['created_at'],
            "reviewers": [ self.get_disocrd_member_id(reviewer['login']) for reviewer in response['requested_reviewers']],
        } for response in responses]

        return pull_requests
    
    def get_diff(self, repo, number):
        headers = self.headers
        headers['Accept'] = 'application/vnd.github.v3.diff'
        return requests.get(f"{self.url}/repos/{self.owner}/{repo}/pulls/{number}", headers=headers)
    
    def comment_to_pull_request(self, repo, number, body):
        headers = self.headers
        headers['Accept'] = 'application/vnd.github.v3+json'
        data = {
            'body': body
        }
        return requests.post(f"{self.url}/repos/{self.owner}/{repo}/issues/{number}/comments", headers=self.headers, data=json.dumps(data))

    def assign_reviewer(self, repo, number, user):
        headers = self.headers
        headers['Accept'] = 'application/vnd.github.v3+json'
        data = {
            'reviewers': self.reviewer.copy()
        }
        if user:
            data['reviewers'].remove(user)
            return requests.post(f"{self.url}/repos/{self.owner}/{repo}/pulls/{number}/requested_reviewers", headers=headers, data=json.dumps(data))
        else:
            return [{'requested_reviewers': []}]