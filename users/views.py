from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.
from django.template.response import TemplateResponse
from django.views import View

from users.forms import LoginForm


class LoginView(View):

    def get(self, request):
        return TemplateResponse(request, 'users/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        ctx = {'form': form, 'message': None}

        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('learning_logs:index')
        else:
            ctx.update({'message': "Your username and password didn't match. Please try again."})
        return TemplateResponse(request, 'users/login.html', ctx)
