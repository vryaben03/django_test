import requests
import json, os
import pandas as pd
from datetime import datetime
import time

class HHParser:
    def __init__(self):
        self.base_url = 'https://api.hh.ru/vacancies'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def parse_salary(self, salary_data):
        """Парсит информацию о зарплате"""
        if not salary_data:
            return {'min': None, 'max': None, 'currency': None}
        
        salary_from = salary_data.get('from')
        salary_to = salary_data.get('to')
        currency = salary_data.get('currency')
        
        # Конвертируем в числа если есть значения
        if salary_from:
            salary_from = float(salary_from)
        if salary_to:
            salary_to = float(salary_to)
        
        return {
            'min': salary_from,
            'max': salary_to,
            'currency': currency
        }
    
    def get_vacancies(self, job_title, pages=3):
        """Получает вакансии с HH API"""
        all_vacancies = []
        
        for page in range(pages):
            params = {
                'text': job_title,
                'area': 1,  # Москва
                'page': page,
                'per_page': 50,  # Максимум на странице
                'only_with_salary': True  # Только с указанной зарплатой
            }
            
            try:
                response = requests.get(self.base_url, params=params, headers=self.headers)
                response.raise_for_status()
                data = response.json()
                
                vacancies = data.get('items', [])
                
                for vacancy in vacancies:
                    parsed_vacancy = {
                        'name': vacancy.get('name'),
                        'salary': self.parse_salary(vacancy.get('salary')),
                        'url': vacancy.get('alternate_url'),
                        'website': 'hh.ru',
                        'employer': vacancy.get('employer', {}).get('name'),
                        'experience': vacancy.get('experience', {}).get('name'),
                        'employment': vacancy.get('employment', {}).get('name'),
                        'published_at': vacancy.get('published_at')
                    }
                    all_vacancies.append(parsed_vacancy)
                
                # Проверяем есть ли еще страницы
                if page >= data.get('pages', 1) - 1:
                    break
                    
                # Задержка чтобы не блокировали
                time.sleep(0.5)
                
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при запросе страницы {page}: {e}")
                continue
        
        return all_vacancies
    
    def save_to_json(self, data, filename_prefix):
        """Сохраняет данные в JSON файл"""
        if not os.path.exists('hh_data'):
            os.makedirs('hh_data')
        
        filename = f'hh_data/{filename_prefix}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def create_dataframe(self, vacancies):
        """Создает pandas DataFrame из вакансий"""
        if not vacancies:
            return pd.DataFrame()
        
        # Подготавливаем данные для DataFrame
        df_data = []
        for vac in vacancies:
            df_data.append({
                'Вакансия': vac['name'],
                'Зарплата_от': vac['salary']['min'],
                'Зарплата_до': vac['salary']['max'],
                'Валюта': vac['salary']['currency'],
                'Работодатель': vac['employer'],
                'Ссылка': vac['url'],
                'Опыт': vac['experience'],
                'Тип_занятости': vac['employment'],
                'Сайт': vac['website']
            })
        
        return pd.DataFrame(df_data)