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

	url(r'^list/$', views.list_files, name='list_files'),
	url(r'^list/(?P<page>\d+)/$', views.list_files, name='list_files'),

	url(r'^file/(?P<pk>\d+)/$', views.file, name='file'),
	url(r'^file/(?P<pk>\d+)/new_chapter/(?P<new_chapter>\d+)$', views.file, name='file'),
	url(r'^file/new/$', views.new_file, name='new_file'),

	url(r'^chapter/(?P<pk>\d+)/$', views.chapter, name='chapter'),
	url(r'^chapter/(?P<pk>\d+)/edit/(?P<edit>\d+)$', views.chapter, name='chapter'),

]
