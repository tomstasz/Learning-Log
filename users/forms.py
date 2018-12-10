from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(label='login', max_length=64)
    password = forms.CharField(label='hasło', max_length=64, widget=forms.PasswordInput)