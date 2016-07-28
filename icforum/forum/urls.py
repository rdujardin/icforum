from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),

	url(r'^tag/(?P<pk>\d+)/$', views.tag, name='tag'),
	url(r'^topic/(?P<pk>\d+)/$', views.topic, name='topic'),

	url(r'^user/(?P<pk>\d+)/$', views.user, name='user'),
]
