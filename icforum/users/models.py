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

class Profile(models.Model):
	NOTIFY_CHOICES = (
		('notify_all', _('Notify every action on the forum')),
		('notify_participated_topics_every_mail', _('Notify updates on participated topics and every mail')),
		('notify_explicitly_chosen_topics_every_mail', _('Notify updates on explicitly chosen topics and every mail')),
		('notify_nothing', _('Notify nothing')),
	)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	signup_date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Signed up'))
	banned = models.BooleanField(default=False, verbose_name=_('Is banned'))
	avatar = models.ImageField(upload_to='avatars/', verbose_name=_('Avatar'), blank=True, null=True)
	notify = models.CharField(max_length=100, choices=NOTIFY_CHOICES, default='notify_all')

	def __str__(self):
		return self.user.username
