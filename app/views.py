from django.shortcuts import render, redirect

# Create your views here.

from django.shortcuts import render
from .hh_parser import HHParser
from .forms import HHParserForm
from .forms import GitHubUserForm, GitHubTokenForm
from .github_api import GitHubAPI
from .vk_api import VKAPI
import os, json
from datetime import datetime
def home(request):
    """Главная страница со списком заданий"""
    assignments = [
        {
            'title': 'GitHub API Integration',
            'description': 'Получение репозиториев пользователя GitHub и сохранение в JSON',
            'url': 'github_api_home',
            'icon': '📊',
            'status': 'active'
        },
        {
            'title': 'VK API - Мои данные',
            'description': 'Получение базовой информации из VK через API',
            'url': 'vk_api_home',
            'icon': '👥',
            'status': 'active'
        },
        {
            'title': 'HH.ru Parser - Вакансии',
            'description': 'Парсинг вакансий с HeadHunter с анализом зарплат',
            'url': 'hh_parser_home',
            'icon': '💼',
            'status': 'active'
        }
    ]
    
    return render(request, 'app/index.html', {'assignments': assignments})

def github_api_home(request):
    """Домашняя страница задания GitHub API"""
    if request.method == 'POST':
        form = GitHubTokenForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            request.session['github_token'] = token
            return redirect('get_repos')
    else:
        form = GitHubTokenForm()
    
    return render(request, 'app/github_api_home.html', {'form': form})

def get_repos(request):
    """Страница для получения репозиториев"""
    # Получаем токен из сессии
    token = request.session.get('github_token')
    
    # Если токена нет - просим ввести
    if not token:
        return redirect('home')
    
    if request.method == 'POST':
        form = GitHubUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            
            # Используем GitHub API
            github_api = GitHubAPI(token)
            repos_data = github_api.get_user_repos(username)
            
            if 'error' in repos_data:
                return render(request, 'app/repos.html', {
                    'form': form,
                    'error': repos_data['error']
                })
            
            # Сохраняем в JSON файл
            filename = github_api.save_to_json(repos_data, username)
            
            # Формируем данные для отображения
            repos_info = []
            for repo in repos_data:
                repos_info.append({
                    'name': repo.get('name', ''),
                    'description': repo.get('description', ''),
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'url': repo.get('html_url', ''),
                    'language': repo.get('language', '')
                })
            
            return render(request, 'app/repos.html', {
                'form': form,
                'repos': repos_info,
                'username': username,
                'filename': filename,
                'repos_count': len(repos_info)
            })
    else:
        form = GitHubUserForm()
    
    return render(request, 'app/repos.html', {'form': form})

def clear_token(request):
    """Очистка токена из сессии"""
    if 'github_token' in request.session:
        del request.session['github_token']
    return redirect('home')

def vk_get_token(request):
    """Страница помощи с получением VK токена"""
    # Используем тестовый APP ID который точно работает
    TEST_APP_ID = 6121396
    
    auth_url = f"https://oauth.vk.com/authorize?client_id={TEST_APP_ID}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=offline&response_type=token&v=5.131"
    
    return render(request, 'github_app/vk_get_token.html', {
        'auth_url': auth_url,
        'app_id': TEST_APP_ID
    })

def vk_api_home(request):
    """Домашняя страница VK API"""
    if request.method == 'POST':
        access_token = request.POST.get('access_token')
        if access_token:
            # Проверяем токен
            vk_api = VKAPI(access_token)
            user_info = vk_api.test_token()
            
            if 'error' in user_info:
                return render(request, 'github_app/vk_api_home.html', {
                    'error': f"Ошибка: {user_info['error']}",
                    'access_token': access_token
                })
            
            # Сохраняем в сессию
            request.session['vk_access_token'] = access_token
            if 'response' in user_info and user_info['response']:
                request.session['vk_user'] = user_info['response'][0]
            
            return redirect('get_vk_basic_info')
    
    return render(request, 'app/vk_api_home.html')

def get_vk_basic_info(request):
    """Получаем базовую информацию"""
    access_token = request.session.get('vk_access_token')
    
    if not access_token:
        return redirect('vk_api_home')
    
    vk_api = VKAPI(access_token)
    user_data = vk_api.get_user_info()
    
    if 'error' in user_data:
        return render(request, 'app/vk_basic_info.html', {
            'error': user_data['error']
        })
    
    # Сохраняем в JSON
    filename = None
    if 'response' in user_data and user_data['response']:
        user_id = user_data['response'][0]['id']
        if not os.path.exists('vk_data'):
            os.makedirs('vk_data')
        filename = f'vk_data/user_{user_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
    
    user_profile = user_data.get('response', [{}])[0] if 'response' in user_data else {}
    
    return render(request, 'app/vk_basic_info.html', {
        'profile': user_profile,
        'filename': filename
    })

def vk_get_token(request):
    """Страница для получения VK токена"""
    
    
    auth_url = f"https://oauth.vk.com/authorize?client_id=6121396&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=email,photos,friends&response_type=token&v=5.131"
    
    return render(request, 'app/vk_get_token.html', {
        'auth_url': auth_url
    })

def hh_parser_home(request):
    """Главная страница HH парсера"""
    if request.method == 'POST':
        form = HHParserForm(request.POST)
        if form.is_valid():
            job_title = form.cleaned_data['job_title']
            pages = form.cleaned_data['pages']
            
            # Сохраняем в сессию
            request.session['hh_job_title'] = job_title
            request.session['hh_pages'] = pages
            
            return redirect('hh_parser_results')
    else:
        form = HHParserForm()
    
    return render(request, 'app/hh_parser_home.html', {'form': form})

def hh_parser_results(request):
    """Страница с результатами парсинга"""
    job_title = request.session.get('hh_job_title')
    pages = request.session.get('hh_pages', 3)
    
    if not job_title:
        return redirect('hh_parser_home')
    
    parser = HHParser()
    
    # Получаем вакансии
    vacancies = parser.get_vacancies(job_title, pages)
    
    # Сохраняем в JSON
    filename = parser.save_to_json(vacancies, f'hh_{job_title.replace(" ", "_")}')
    
    # Создаем DataFrame
    df = parser.create_dataframe(vacancies)
    
    # Подготавливаем данные для отображения
    vacancies_for_display = []
    for vac in vacancies[:20]:  # Показываем первые 20
        salary_info = ""
        if vac['salary']['min'] or vac['salary']['max']:
            if vac['salary']['min'] and vac['salary']['max']:
                salary_info = f"{vac['salary']['min']:,.0f} - {vac['salary']['max']:,.0f} {vac['salary']['currency']}"
            elif vac['salary']['min']:
                salary_info = f"от {vac['salary']['min']:,.0f} {vac['salary']['currency']}"
            elif vac['salary']['max']:
                salary_info = f"до {vac['salary']['max']:,.0f} {vac['salary']['currency']}"
        else:
            salary_info = "не указана"
        
        vacancies_for_display.append({
            'name': vac['name'],
            'salary': salary_info,
            'url': vac['url'],
            'employer': vac['employer'],
            'experience': vac['experience']
        })
    
    # Статистика по зарплатам
    salary_stats = {}
    if not df.empty:
        salary_stats = {
            'avg_min': df['Зарплата_от'].mean(),
            'avg_max': df['Зарплата_до'].mean(),
            'total_vacancies': len(df)
        }
    
    return render(request, 'app/hh_parser_results.html', {
        'job_title': job_title,
        'pages': pages,
        'vacancies': vacancies_for_display,
        'filename': filename,
        'total_vacancies': len(vacancies),
        'salary_stats': salary_stats,
        'dataframe_html': df.to_html(classes='table table-striped', index=False) if not df.empty else None
    })