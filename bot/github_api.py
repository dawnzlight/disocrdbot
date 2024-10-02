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

    def get_pull_requests(self, repo):

        headers = self.headers
        headers['Accept'] = 'application/vnd.github.v3+json'

        responses = requests.get(f"{self.url}/repos/{self.owner}/{repo}/pulls", headers=self.headers).json()

        pull_requests = [ {
            'url': response['url'],
            'title': response['title'],
            'number': response['number'],
            'user':response['user']['login'],
            "created_at": response['created_at'],
            "reviewers": [ self.discord_member_id[reviewer['login']] for reviewer in response['requested_reviewers']],
        } for response in responses]

        return pull_requests
    
    def get_diff(self, repo, number):
        headers = self.headers
        headers['Accept'] = 'application/vnd.github.v3.diff'
        return requests.get(f"{self.url}/repos/{self.owner}/{repo}/pulls/{number}", headers=self.headers)
    
    def comment_to_pull_request(self, repo, number, body):

        data = {
            'body': body
        }
        requests.post(f"{self.url}/repos/{self.owner}/{repo}/issues/{number}/comments", headers=self.headers, data=data)