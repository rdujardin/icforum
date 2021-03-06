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

from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^signin/$', views.sign_in, name='sign_in'),
	url(r'^signout/$', views.sign_out, name='sign_out'),

	url(r'^set_language/(?P<lang>[a-zA-Z0-9-_]+)/$', views.set_language, name='set_language'),

	url(r'^user/(?P<pk>\d+)/$', views.user, name='user'),

	# TODO : check security before activate this api
	#url(r'^api/', include('users.api.urls')),
]
