import requests
import json
import os
from datetime import datetime

class VKAPI:
    def __init__(self, access_token=None):
        self.access_token = access_token
        self.base_url = 'https://api.vk.com/method'
        self.api_version = '5.131'
    
    def get_user_info(self):
        """Получает базовую информацию о пользователе"""
        method = 'users.get'
        url = f'{self.base_url}/{method}'
        
        params = {
            'access_token': self.access_token,
            'v': self.api_version,
            'fields': 'photo_200,sex,bdate,city,country'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'error' in data:
                error_msg = data['error'].get('error_msg', 'Unknown error')
                return {'error': error_msg}
            
            return data
            
        except requests.exceptions.RequestException as e:
            return {'error': f'Ошибка сети: {str(e)}'}
    
    def test_token(self):
        """Проверяет валидность токена"""
        return self.get_user_info()