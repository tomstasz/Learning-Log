from django.conf.urls import url
from django.contrib.auth import login


app_name = 'users'

urlpatterns = [
    url(r'^login/$', login, {'template_name': 'users/login.html'}, name='login'),
]