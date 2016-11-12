# Copyright 2016 Infinite Connection
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
