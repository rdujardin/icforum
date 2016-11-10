from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),

	url(r'^mail/$', views.mail, name='mail'),
	url(r'^mail/page/(?P<page>\d+)/$', views.mail, name='mail'),
	url(r'^mail/new/$', views.new_mail, name='new_mail'),
	url(r'^mail/new/(?P<pk>\d+)/$', views.new_mail, name='new_mail'),

	url(r'^tag/(?P<pk>\d+)/$', views.tag, name='tag'),
	url(r'^tag/(?P<pk>\d+)/page/(?P<page>\d+)/$', views.tag, name='tag'),

	url(r'^topic/new/$', views.new_topic, name='new_topic'),
	url(r'^topic/(?P<pk>\d+)/$', views.topic, name='topic'),
	url(r'^topic/(?P<pk>\d+)/page/(?P<page>\d+)/$', views.topic, name='topic'),
	url(r'^topic/(?P<pk>\d+)/edit/(?P<edit_message>\d+)/$', views.topic, name='topic'),

]
