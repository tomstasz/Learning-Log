"""Defines URL patterns for learning_logs."""

from django.conf.urls import url
from . import views


app_name = 'learning_logs'

urlpatterns = [
    # Home page
    url(r'^$', views.index, name='index'),

    # Show all topics
    url(r'^topics/$', views.topics, name='topics'),
    url(r'topics/(?P<topic_id>(\d)+)$', views.topic, name='topic'),
    url(r'^new_topic/$', views.NewTopic.as_view(), name='new_topic'),
    url(r'^new_entry/(?P<topic_id>(\d)+)/$', views.NewEntry.as_view(), name='new_entry'),
    url(r'^edit_entry/(?P<entry_id>(\d)+)/$', views.edit_entry, name='edit_entry'),
]