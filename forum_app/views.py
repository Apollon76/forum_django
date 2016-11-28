from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .forms import RegistrationForm, LoginForm, PostForm
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
            new_user = User(username=form_data['nickname'], password=form_data['password'], email=form_data['email'], is_staff=False) #, is_admin=False, )
            if not User.objects.filter(username=form.cleaned_data['nickname']).exists():
                new_user.save()
                return HttpResponseRedirect('../')
            else:
                return render(request, 'registration.html', {'form': RegistrationForm(), 'error_message': 'User with this nickname has already been registered.'})
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
    return render(request, 'section.html', {'section': cur_section})


def thread_view(request, section_id, thread_id):
    cur_thread = Thread.objects.get(pk=thread_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid() and request.user.is_authenticated():
            new_message = Post(data=form.cleaned_data['data'], author=request.user)
            new_message.save()
            cur_thread.posts.add(new_message)
    return render(request, 'thread.html', {'thread': cur_thread, 'post_form': PostForm()})
