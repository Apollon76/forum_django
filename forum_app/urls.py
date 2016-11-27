from django.conf.urls import url

from . import views

urlpatterns = [url(r'^$', views.index, name='index'),
               url(r'^reg/$', views.registration, name='registration'),
               url(r'^login/$', views.login_page, name='login'),
               url(r'^logout/$', views.logout_view, name='logout'),
               url(r'^sections/(?P<id>[0-9]+)/$', views.section_view, name='section'),
               url(r'^sections/(?P<section_id>[0-9]+)/(?P<thread_id>[0-9]+)/$', views.thread_view, name='thread'),
               ]
