from django import forms

class LoginForm(forms.Form):
    user_name = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput, required=True)
    next_page = forms.CharField(label='Next Page', widget=forms.HiddenInput, initial="/")
