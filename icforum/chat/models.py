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

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

class Room(models.Model):
	name = models.CharField(max_length=100, verbose_name=_('Name'), blank=True)
	members = models.ManyToManyField(User, verbose_name=_('Members'))

	def __str__(self):
		return self.name if self.name else ', '.join(self.members.all())

class ChatMessage(models.Model):
	room = models.ForeignKey(Room, related_name='messages', verbose_name=_('Room'))
	author = models.ForeignKey(User, related_name='chat_messages', verbose_name=_('Author'))
	date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))
	content = models.TextField(verbose_name=_('Content'))

	def __str__(self):
		return self.content
