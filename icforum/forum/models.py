from django.db import models
from django.contrib.auth.models import User, Group

#
# Users
#

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	signup_date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Signed up')
	banned = models.BooleanField(default=False, verbose_name='Is banned')
	avatar = models.ImageField(upload_to='avatars/', verbose_name='Avatar', blank=True, null=True)

	def __str__(self):
		return self.user.username

#
# Forums
#

class Tag(models.Model):
	name = models.CharField(max_length=100, verbose_name='Name')
	main = models.BooleanField(default=False, verbose_name='On Homepage')
	only_for = models.ManyToManyField(Group, verbose_name='Allowed Groups')
	cover_image = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.name

class Topic(models.Model):
	title = models.CharField(max_length=100, verbose_name='Title')
	author = models.ForeignKey(User, related_name='created_topics', verbose_name='Author')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
	updated = models.DateTimeField(auto_now_add=True, verbose_name='Updated')
	tags = models.ManyToManyField(Tag, verbose_name='Tags')
	post_it = models.BooleanField(default=False, verbose_name='Post-it')
	closed = models.BooleanField(default=False, verbose_name='Closed')

	def __str__(self):
		return self.title

class Message(models.Model):

	class Meta:
		permissions = (
			('edit_not_owned_message', 'Can edit messages authored by someone else'),
		)

	topic = models.ForeignKey(Topic, related_name='messages', verbose_name='Topic')
	author = models.ForeignKey(User, related_name='posted_messages', verbose_name='Author')
	content = models.TextField(verbose_name='Content')
	posted = models.DateTimeField(auto_now_add=True, verbose_name='Posted')
	edited = models.DateTimeField(auto_now_add=True, verbose_name='Edited')

	def __str__(self):
		return str(self.topic) + ' : ' + str(self.author) + ' : ' + self.content[:35] + '(...)'