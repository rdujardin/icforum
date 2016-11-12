import bleach
from urllib.parse import urlparse
from django.conf import settings
from django.shortcuts import render
from django.utils.translation import get_language

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
	return render(request, template, extra)