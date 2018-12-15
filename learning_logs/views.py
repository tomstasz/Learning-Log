from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from learning_logs.models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.views import View


def index(request):
    return render(request, 'learning_logs/index.html')


def check_topic_owner(request, topic_to_check):
    if topic_to_check.owner != request.user:
        raise Http404



@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    ctx = {
        'topics': topics,
    }

    return render(request, 'learning_logs/topics.html', ctx)


@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    check_topic_owner(request, topic)
    entries = topic.entry_set.order_by('-date_added')
    ctx = {
        'entries': entries,
        'topic': topic,
    }
    return render(request, 'learning_logs/topic.html', ctx)


class NewTopic(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request):
        form = TopicForm
        ctx = {
            'form': form
        }
        return render(request, 'learning_logs/new_topic.html', ctx)

    def post(self, request):
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))


class NewEntry(LoginRequiredMixin, View):
    login_url = 'users:login'

    def get(self, request, topic_id):
        topic = Topic.objects.get(id=topic_id)
        form = EntryForm()
        ctx = {
            'form': form,
            'topic': topic
        }
        return render(request, 'learning_logs/new_entry.html', ctx)

    def post(self, request, topic_id):
        topic = Topic.objects.get(id=topic_id)
        form = EntryForm(data=request.POST)
        check_topic_owner(request, topic)
        if form.is_valid():
            new_entry = form.save(commit=False)  # commit=False, without saving to database yet
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    check_topic_owner(request, topic)

    if request.method == 'GET':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)  # instance=entry, form is pre-filled with existing info
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    ctx = {
        'entry': entry,
        'topic': topic,
        'form': form
    }

    return render(request, 'learning_logs/edit_entry.html', ctx)
