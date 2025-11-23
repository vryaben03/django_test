from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('repos/', views.get_repos, name='get_repos'),
    path('clear/', views.clear_token, name='clear_token'),
]