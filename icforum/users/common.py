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

import bleach
from urllib.parse import urlparse
from django.conf import settings
from django.shortcuts import render
from django.utils.translation import get_language
from chat.models import *
from forum.models import *
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail

def sanitize_html(content):
	def filter_iframe_src(name, value):
		if name in ('width', 'height', 'frameborder', 'allowfullscreen'):
			return True
		elif name == 'src':
			p = urlparse(value)
			return (not p.netloc) or p.netloc == 'youtube.com' or p.netloc == 'www.youtube.com'
		else:
			return False

	return bleach.clean(content,
		tags=['iframe', 'a', 'abbr', 'acronym', 'address', 'area', 'b', 'bdo', 'big', 'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em', 'fieldset', 'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'input', 'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol', 'optgroup', 'option', 'p', 'pre', 'q', 's', 'samp', 'select', 'small', 'span', 'strike', 'strong', 'sub', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'u', 'tr', 'tt', 'u', 'ul', 'var'],
		attributes={
			'*': ['class', 'id', 'style'],
			'iframe': filter_iframe_src,
			'a': ['href'],
			'font': ['color', 'face', 'size'],
			'img': ['align', 'alt', 'height', 'src', 'title', 'width'],
		},
		styles=['color', 'text-align', 'background-color']
	)


def _render(request, template, extra):
	extra['ic_forum_version'] = settings.IC_FORUM_VERSION
	extra['signed_in_user'] = request.user.username if request.user.is_authenticated() else None
	extra['current_language'] = get_language()
	if request.user.is_authenticated():
		extra['chat_rooms'] = Room.objects.filter(members=request.user)
	return render(request, template, extra)


def notify_user_email(type, pk, page, src_user, user):
	topic = Topic.objects.get(pk=pk)
	if type == 'mail_new_or_edited_message':
		title = 'Notification : nouveaux messages privés'
		content_text = '{} a répondu dans la conversation privée "{}" ({}/topic/{}/page/{}/).'.format(src_user.username, topic.title, settings.IC_FORUM_URL, topic.pk, page)
		content_html = '<a href="{}/user/{}/">{}</a> a répondu dans la conversation privée <a href="{}/topic/{}/page/{}/">{}</a>.'.format(settings.IC_FORUM_URL, src_user.pk, src_user.username, settings.IC_FORUM_URL, topic.pk, page, topic.title)
	elif type == 'mail_new_mail':
		title = 'Notification : nouveaux messages privés'
		content_text = '{} vous a envoyé un nouveau message privé de titre "{}" ({}/topic/{}/).'.format(src_user.username, topic.title, settings.IC_FORUM_URL, topic.pk)
		content_html = '<a href="{}/user/{}/">{}</a> vous a envoyé un nouveau message privé de titre <a href="{}/topic/{}/">{}</a>.'.format(settings.IC_FORUM_URL, src_user.pk, src_user.username, settings.IC_FORUM_URL, topic.pk, topic.title)
	elif type == 'topic_new_or_edited_message':
		title = 'Notification : nouveaux messages sur le forum'
		content_text = '{} a répondu dans le sujet "{}" ({}/topic/{}/page/{}/).'.format(src_user.username, topic.title, settings.IC_FORUM_URL, topic.pk, page)
		content_html = '<a href="{}/user/{}/">{}</a> a répondu dans le sujet <a href="{}/topic/{}/page/{}/">{}</a>.'.format(settings.IC_FORUM_URL, src_user.pk, src_user.username, settings.IC_FORUM_URL, topic.pk, page, topic.title)
	elif type == 'topic_new_topic':
		title = 'Notification : nouveau sujet sur le forum'
		content_text = '{} a créé un nouveau sujet "{}" ({}/topic/{}/).'.format(src_user.username, topic.title, settings.IC_FORUM_URL, topic.pk)
		content_html = '<a href="{}/user/{}/">{}</a> a créé un nouveau sujet <a href="{}/topic/{}/">{}</a>.'.format(settings.IC_FORUM_URL, src_user.pk, src_user.username, settings.IC_FORUM_URL, topic.pk, topic.title)
	else:
		return

	text_msg = '{}\n\n{}\n\nCe message de notification vous est envoyé parce que vous êtes membre du forum {} ({}). Pour modifier vos paramètres de notification, rendez-vous sur votre page de profil ({}/user/{}/).'.format(title, content_text, settings.IC_FORUM_NAME, settings.IC_FORUM_URL, settings.IC_FORUM_URL, user.pk)
	html_msg = '''
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<title>{}</title>
	</head>
	<body>
		<p>{}</p>
		<hr />
		<p>Ce message de notification vous est envoyé parce que vous êtes membre du <a href="{}">forum {}</a>. Pour modifier vos paramètres de notification, rendez-vous <a href="{}/user/{}/">sur votre page de profil.</p>
	</body>
</html>'''.format(title, content_html, settings.IC_FORUM_URL, settings.IC_FORUM_NAME, settings.IC_FORUM_URL, user.pk)
	send_mail(title, text_msg, settings.NOTIFICATION_EMAIL, [user.email], fail_silently=False, html_message=html_msg)


def notify(type, pk, page, src_user):
	for user in User.objects.all():
		if not user == src_user:
			profile = Profile.objects.get(user=user)
			if (not profile.notify == 'notify_nothing') and user != src_user and user.email:
				topic = Topic.objects.get(pk=pk)
				if has_access_topic(topic, user):
					if type == 'mail_new_or_edited_message':
						if (user in topic.private_viewers.all()) and (profile.notify == 'notify_all' or profile.notify == 'notify_participated_topics_every_mail' or profile.notify == 'notify_explicitly_chosen_topics_every_mail'):
							notify_user_email(type, pk, page, src_user, user)
					elif type == 'mail_new_mail':
						if (user in topic.private_viewers.all()) and (profile.notify == 'notify_all' or profile.notify == 'notify_participated_topics_every_mail' or profile.notify == 'notify_explicitly_chosen_topics_every_mail'):
							notify_user_email(type, pk, page, src_user, user)
					elif type == 'topic_new_or_edited_message':
						participated = False
						if Message.objects.filter(topic=topic, author=user):
							participated = True
						chosen = user in topic.notify.all()
						if (profile.notify == 'notify_all') or (profile.notify == 'notify_participated_topics_every_mail' and participated) or (profile.notify == 'notify_explicitly_chosen_topics_every_mail' and chosen):
							notify_user_email(type, pk, page, src_user, user)
					elif type == 'topic_new_topic':
						if profile.notify == 'notify_all':
							notify_user_email(type, pk, page, src_user, user)


def has_access_topic(topic, user):
	# Check that topic does not belong to a tag only for a group the user does not belong to
	for tag in topic.tags.all():
		if tag.only_for.all():
			allowed = False
			for allowed_group in tag.only_for.all():
				if allowed_group in user.groups.all():
					allowed = True
			if not allowed:
				return False

	# Check if the topic is public or if the user can see it
	private_viewers = topic.private_viewers.all()
	return (not private_viewers) or user in private_viewers


def has_access_file(file, user):
	# Check that file does not belong to a tag only for a group the user does not belong to
	for tag in file.tags.all():
		if tag.only_for.all():
			allowed = False
			for allowed_group in tag.only_for.all():
				if allowed_group in user.groups.all():
					allowed = True
			if not allowed:
				return False
	return True