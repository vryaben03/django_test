from django.shortcuts import render, redirect

# Create your views here.

from django.shortcuts import render

from .forms import GitHubUserForm, GitHubTokenForm
from .github_api import GitHubAPI

def home(request):
    """Главная страница с формой ввода токена"""
    if request.method == 'POST':
        form = GitHubTokenForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['token']
            # Сохраняем токен в СЕССИЮ
            request.session['github_token'] = token
            return redirect('get_repos')
    else:
        form = GitHubTokenForm()
    
    return render(request, 'app/index.html', {'form': form})

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

