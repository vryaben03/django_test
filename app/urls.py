from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница с заданиями
    path('github-api/', views.github_api_home, name='github_api_home'),  # Страница GitHub API
    path('github-api/repos/', views.get_repos, name='get_repos'),
    path('github-api/clear/', views.clear_token, name='clear_token'),
    path('vk-api/', views.vk_api_home, name='vk_api_home'),
    path('vk-api/basic-info/', views.get_vk_basic_info, name='get_vk_basic_info'),
    path('vk-api/get-token/', views.vk_get_token, name='vk_get_token'),
    path('hh-parser/', views.hh_parser_home, name='hh_parser_home'),
    path('hh-parser/results/', views.hh_parser_results, name='hh_parser_results'),
]