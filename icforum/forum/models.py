from django.db import models

#
# Users
#

class Group(models.Model):
	name = models.CharField(max_length=100, verbose_name='Name')

	def __str__(self):
		return self.name

class User(models.Model):
	name = models.CharField(max_length=100, verbose_name='Name')
	password = models.CharField(max_length=100, verbose_name='Password')
	signup_date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name='Signed up')
	groups = models.ManyToManyField(Group)

	def __str__(self):
		return self.name

#
# Forums
#

class Tag(models.Model):
	name = models.CharField(max_length=100, verbose_name='Name')
	main = models.BooleanField(default=False, verbose_name='On Homepage')

	def __str__(self):
		return self.name

class Topic(models.Model):
	title = models.CharField(max_length=100, verbose_name='Title')
	author = models.ForeignKey(User, related_name='created_topics', verbose_name='Author')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
	updated = models.DateTimeField(auto_now_add=True, verbose_name='Updated')
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return self.title

class Message(models.Model):
	topic = models.ForeignKey(Topic, related_name='messages', verbose_name='Topic')
	author = models.ForeignKey(User, related_name='posted_messages', verbose_name='Author')
	content = models.TextField(verbose_name='Content')
	posted = models.DateTimeField(auto_now_add=True, verbose_name='Posted')
	edited = models.DateTimeField(auto_now_add=True, verbose_name='Edited')

	def __str__(self):
		return self.topic + ' : ' + self.author + ' : ' + self.content[:35] + '(...)'