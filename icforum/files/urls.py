from django.conf.urls import url
from . import views

urlpatterns = [

	url(r'^list/$', views.list_files, name='list_files'),
	url(r'^list/(?P<page>\d+)/$', views.list_files, name='list_files'),

	url(r'^file/(?P<pk>\d+)/$', views.file, name='file'),

	url(r'^chapter/(?P<pk>\d+)/$', views.chapter, name='chapter'),
	url(r'^chapter/(?P<pk>\d+)/edit/(?P<edit>\d+)$', views.chapter, name='chapter'),

]
