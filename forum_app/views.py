from math import ceil

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import *
from .models import Section, Thread, Post


def index(request):
    registered_users = User.objects.all()
    sections = Section.objects.all()
    return render(request, 'index.html', {'sections': sections, 'registered_users': ', '.join(map(str, registered_users))})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            if not User.objects.filter(username=form.cleaned_data['nickname']).exists():
                new_user = User.objects.create_user(form_data['nickname'], form_data['email'], form_data['password'])
                new_user.save()
                return HttpResponseRedirect('../')
            else:
                return render(request, 'registration.html', {'form': RegistrationForm(),
                                                             'error_message': 'User with this nickname has already been registered.'})
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('../')
        else:
            return render(request, 'login.html', {'error_message': 'Incorrect username or password.'})
    login_form = LoginForm()
    return render(request, 'login.html', {'form': login_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('../')


def section_view(request, id):
    cur_section = Section.objects.get(pk=id)
    section_threads = cur_section.threads.all().order_by('-id')
    return render(request, 'section.html', {'section': cur_section, 'section_threads': section_threads})


@login_required(login_url='/forum_app/login')
@require_POST
def post_new_thread(request, section_id):
    cur_section = Section.objects.get(pk=section_id)
    thread_form = NewThreadForm(request.POST)
    post_form = PostForm(request.POST)
    if thread_form.is_valid() and post_form.is_valid():
        new_thread = Thread(name=thread_form.cleaned_data['name'])
        new_thread.save()
        cur_section.threads.add(new_thread)
        post_message(request, section_id, new_thread.id)
        return HttpResponseRedirect('../../')


@login_required(login_url='/forum_app/login')
def new_thread_view(request, section_id):
    return render(request, 'new_thread.html', {'thread_form': NewThreadForm(), 'post_form': PostForm()})


@require_POST
def post_message(request, section_id, thread_id):
    cur_thread = Thread.objects.get(pk=thread_id)
    form = PostForm(request.POST)
    if form.is_valid() and request.user.is_authenticated():
        new_message = Post(data=form.cleaned_data['data'], author=request.user)
        new_message.save()
        cur_thread.posts.add(new_message)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def thread_view(request, section_id, thread_id):
    cur_thread = Thread.objects.get(pk=thread_id)
    posts_on_page = cur_thread.posts.all().order_by('-id')
    cur_page = 0
    if 'page' in request.GET:
        cur_page = int(request.GET['page'])
    posts_number = 10
    max_page = (len(posts_on_page) - 1) // posts_number
    max_page = max(max_page, 0)
    return render(request, 'thread.html', {'thread': cur_thread, 'post_form': PostForm(),
                                           'posts': posts_on_page[posts_number * cur_page:min(len(posts_on_page), posts_number * (cur_page + 1))],
                                           'cur_page': cur_page, 'max_page': max_page})


@login_required(login_url='/forum_app/login')
def delete_post(request, section_id, thread_id, post_id):
    if request.user.is_staff:
        cur_thread = Thread.objects.get(pk=thread_id)
        post = Post.objects.get(pk=post_id)
        cur_thread.posts.remove(post)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))