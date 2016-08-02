from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),

	url(r'^signin/$', views.sign_in, name='sign_in'),
	url(r'^signout/$', views.sign_out, name='sign_out'),

	url(r'^tag/(?P<pk>\d+)/$', views.tag, name='tag'),

	url(r'^topic/new/$', views.new_topic, name='new_topic'),
	url(r'^topic/(?P<pk>\d+)/$', views.topic, name='topic'),
	url(r'^topic/(?P<pk>\d+)/page/(?P<page>\d+)/$', views.topic, name='topic'),
	url(r'^topic/(?P<pk>\d+)/edit/(?P<edit_message>\d+)/$', views.topic, name='topic'),

	url(r'^user/(?P<pk>\d+)/$', views.user, name='user'),
]
