import django_tables2 as tables
from django_tables2.utils import Accessor

from .models import *

class TagTable(tables.Table):
	class Meta:
		model = Tag
		fields = ['name']

	name = tables.LinkColumn('tag', args=[Accessor('pk')], orderable=False)


class TopicTable(tables.Table):
	class Meta:
		model = Topic
		fields = ['title', 'author', 'created', 'updated', 'tags']

	title = tables.LinkColumn('topic', args=[Accessor('pk')], orderable=False)
	author = tables.LinkColumn('user', args=[Accessor('pk')], orderable=False)
	tags = tables.Column(orderable=False)

	def render_tags(self, value):
		if value:
			return ', '.join([tag.name for tag in value.all()])
		return '-'

class MessageTable(tables.Table):
	class Meta:
		model = Message
		fields = ['author', 'posted', 'content']

	author = tables.LinkColumn('user', args=[Accessor('pk')], orderable=False)
	posted = tables.Column(orderable=False)
	content = tables.Column(orderable=False)
