from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail

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
            if not User.objects.filter(username=form.cleaned_data['nickname']).exists() and \
                    not User.objects.filter(email=form.cleaned_data['email']).exists():
                new_user = User.objects.create_user(form_data['nickname'], form_data['email'], form_data['password'])
                new_user.save()
                '''
                send_mail(
                    'Добро пожаловать',
                    'Here is the message.',
                    'Apollon76@yandex.ru',
                    [form_data['email']],
                    fail_silently=False,
                )
                '''
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'registration.html', {'form': RegistrationForm(),
                                                             'error_message': 'User with this nickname or e-mail has already been registered.'})
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            prev_page = request.GET.get('prev_page')
            if prev_page is None:
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponseRedirect(prev_page)
        else:
            return render(request, 'login.html', {'error_message': 'Incorrect username or password.'})
    login_form = LoginForm()
    return render(request, 'login.html', {'form': login_form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def section_view(request, id):
    cur_section = Section.objects.get(pk=id)
    section_threads = cur_section.threads.all().order_by('-id')
    pages = Paginator(section_threads, 10)
    page_number = request.GET.get('page')
    try:
        cur_page = pages.page(page_number)
    except PageNotAnInteger:
        cur_page = pages.page(1)
    except EmptyPage:
        cur_page = pages.page(pages.num_pages)
    return render(request, 'section.html', {'section': cur_section, 'page': cur_page})


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
        return HttpResponseRedirect(reverse('thread', kwargs={'section_id': section_id, 'thread_id': new_thread.id}))


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
    page_number = request.GET.get('page')
    pages = Paginator(posts_on_page, 10)
    try:
        cur_page = pages.page(page_number)
    except PageNotAnInteger:
        cur_page = pages.page(1)
    except EmptyPage:
        cur_page = pages.page(pages.num_pages)
    return render(request, 'thread.html', {'thread': cur_thread, 'post_form': PostForm(),
                                           'page': cur_page})


def recently_created_thread(request):
    cur_thread = Thread.objects.latest('id')
    if cur_thread is None:
        return JsonResponse({})
    cur_section = Section.objects.filter(threads__id=cur_thread.id)
    if not cur_section.exists():
        return JsonResponse({})
    cur_section = cur_section[0]
    return JsonResponse({'link': reverse('thread', kwargs={'section_id': cur_section.id, 'thread_id': cur_thread.id}),
                         'name': cur_thread.name, })


@login_required(login_url='/forum_app/login')
def delete_post(request, section_id, thread_id, post_id):
    post = Post.objects.get(pk=post_id)
    if request.user.is_staff or post.author == request.user:
        cur_thread = Thread.objects.get(pk=thread_id)
        cur_thread.posts.remove(post)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='/forum_app/login')
def delete_profile(request, user_id):
    if request.user.is_staff or request.user.id == int(user_id):
        cur_user = User.objects.get(pk=user_id)
        cur_user.delete()
    return HttpResponseRedirect(reverse('index'))


def profile(request, user_id):
    cur_user = get_object_or_404(User, id=user_id)
    return render(request, 'profile.html', {'cur_user': cur_user})
