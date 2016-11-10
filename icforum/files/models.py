from django.db import models
from forum.models import Tag

class File(models.Model):

	class Meta:
		permissions = (
			('create_edit_file', 'Can create and edit files'),
		)

	title = models.CharField(max_length=100, verbose_name='Title')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
	updated = models.DateTimeField(auto_now_add=True, verbose_name='Updated')
	tags = models.ManyToManyField(Tag, verbose_name='Tags')

	def __str__(self):
		return self.title

class Chapter(models.Model):

	file = models.ForeignKey(File, related_name='chapters', verbose_name='File')
	position = models.PositiveIntegerField(verbose_name='Position')
	title = models.CharField(max_length=100, verbose_name='Title')
	content = models.TextField(verbose_name='Content')

	def __str__(self):
		return self.title