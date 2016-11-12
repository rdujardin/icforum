from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

#
# Forums
#

class Tag(models.Model):
	name = models.CharField(max_length=100, verbose_name=_('Name'))
	main = models.BooleanField(default=False, verbose_name=_('On Homepage'))
	only_for = models.ManyToManyField(Group, verbose_name=_('Allowed Groups'))
	cover_image = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.name

class Topic(models.Model):
	title = models.CharField(max_length=100, verbose_name=_('Title'))
	author = models.ForeignKey(User, related_name='created_topics', verbose_name=_('Author'))
	created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
	updated = models.DateTimeField(auto_now_add=True, verbose_name=_('Updated'))
	tags = models.ManyToManyField(Tag, verbose_name=_('Tags'))
	private_viewers = models.ManyToManyField(User)
	post_it = models.BooleanField(default=False, verbose_name=_('Post-it'))
	closed = models.BooleanField(default=False, verbose_name=_('Closed'))

	def __str__(self):
		return self.title

class Message(models.Model):

	class Meta:
		permissions = (
			('edit_not_owned_message', _('Can edit messages authored by someone else')),
		)

	topic = models.ForeignKey(Topic, related_name='messages', verbose_name=_('Topic'))
	author = models.ForeignKey(User, related_name='posted_messages', verbose_name=_('Author'))
	content = models.TextField(verbose_name=_('Content'))
	posted = models.DateTimeField(auto_now_add=True, verbose_name=_('Posted'))
	edited = models.DateTimeField(auto_now_add=True, verbose_name=_('Edited'))

	def __str__(self):
		return str(self.topic) + ' : ' + str(self.author) + ' : ' + self.content[:35] + '(...)'
