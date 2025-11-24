from django import forms

class GitHubUserForm(forms.Form):
    username = forms.CharField(
        max_length=100, 
        label='GitHub Username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter GitHub username'})
    )

class GitHubTokenForm(forms.Form):
    token = forms.CharField(
        max_length=100,
        label='GitHub Personal Access Token',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your GitHub token'})
    )

class HHParserForm(forms.Form):
    job_title = forms.CharField(
        max_length=100,
        label='Должность',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Например: Python разработчик'
        })
    )
    pages = forms.IntegerField(
        label='Количество страниц для анализа',
        min_value=1,
        max_value=10,
        initial=3,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'От 1 до 10'
        }),
        help_text="Каждая страница содержит ~50 вакансий"
    )