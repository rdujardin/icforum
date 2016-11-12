from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^signin/$', views.sign_in, name='sign_in'),
	url(r'^signout/$', views.sign_out, name='sign_out'),

	url(r'^set_language/(?P<lang>[a-zA-Z0-9-_]+)/$', views.set_language, name='set_language'),

	url(r'^user/(?P<pk>\d+)/$', views.user, name='user'),
]
