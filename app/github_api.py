import requests
import json
import os
from datetime import datetime

class GitHubAPI:
    def __init__(self, token=None):
        self.token = token
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {token}' if token else '',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def get_user_repos(self, username):
        """Получает список репозиториев пользователя"""
        url = f'{self.base_url}/users/{username}/repos'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    def save_to_json(self, data, username):
        """Сохраняет данные в JSON файл"""
        if not os.path.exists('github_data'):
            os.makedirs('github_data')
        
        filename = f'github_data/{username}_repos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filename