from django.conf.urls import url

from . import views

urlpatterns = [url(r'^$', views.index, name='index'),
               url(r'^reg/$', views.registration, name='registration'),
               url(r'^login/$', views.login_page, name='login'),
               url(r'^logout/$', views.logout_view, name='logout'),
               url(r'^sections/(?P<id>[0-9]+)/$', views.section_view, name='section'),
               url(r'^sections/(?P<section_id>\d+)/(?P<thread_id>[0-9]+)/$', views.thread_view, name='thread'),
               url(r'^sections/(?P<section_id>\d+)/(?P<thread_id>[0-9]+)/submit/$', views.post_message, name='submit_message'),
               url(r'^sections/(?P<section_id>\d+)/new_thread/$', views.new_thread_view, name='new_thread'),
               url(r'^sections/(?P<section_id>\d+)/new_thread/submit/$', views.post_new_thread, name='post_new_thread'),
               url(r'^sections/(?P<section_id>\d+)/(?P<thread_id>\d+)/(?P<post_id>\d+)/delete_post/$', views.delete_post, name='delete_post'),
               url(r'^profile/(?P<user_id>\d+)/$', views.profile, name='profile'),
               url(r'^delete_profile/(?P<user_id>\d+)/$', views.delete_profile, name='delete_profile'),
               url(r'^recently_created_thread/$', views.recently_created_thread, name='recently_created_thread'),
               ]
