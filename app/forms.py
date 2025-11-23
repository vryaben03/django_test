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