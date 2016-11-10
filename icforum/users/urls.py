from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^signin/$', views.sign_in, name='sign_in'),
	url(r'^signout/$', views.sign_out, name='sign_out'),

	url(r'^user/(?P<pk>\d+)/$', views.user, name='user'),
]
