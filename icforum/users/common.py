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