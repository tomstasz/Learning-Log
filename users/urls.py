from django.conf.urls import url
from users.views import LoginView, logout_view, register

app_name = 'users'

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^register/$', register, name='register')
]