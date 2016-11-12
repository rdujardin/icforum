from django.db import models
from forum.models import Tag
from django.utils.translation import ugettext_lazy as _

class File(models.Model):

	class Meta:
		permissions = (
			('create_edit_file', _('Can create and edit files')),
		)

	title = models.CharField(max_length=100, verbose_name=_('Title'))
	created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
	updated = models.DateTimeField(auto_now_add=True, verbose_name=_('Updated'))
	tags = models.ManyToManyField(Tag, verbose_name=_('Tags'))

	def __str__(self):
		return self.title

class Chapter(models.Model):

	file = models.ForeignKey(File, related_name='chapters', verbose_name=_('File'))
	position = models.PositiveIntegerField(verbose_name=_('Position'))
	title = models.CharField(max_length=100, verbose_name=_('Title'))
	content = models.TextField(verbose_name=_('Content'))

	def __str__(self):
		return self.title