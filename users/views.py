from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.
from django.template.response import TemplateResponse
from django.urls import reverse
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


def logout_view(request):
    logout(request)
    return redirect(reverse('learning_logs:index'))


def register(request):

    if request.method == 'GET':
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])  # user enters pass two times to match
            login(request, authenticated_user)
            return redirect(reverse('learning_logs:index'))

    ctx = {'form': form}
    return TemplateResponse(request, 'users/register.html', ctx)
