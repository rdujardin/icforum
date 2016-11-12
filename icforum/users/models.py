from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	signup_date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Signed up'))
	banned = models.BooleanField(default=False, verbose_name=_('Is banned'))
	avatar = models.ImageField(upload_to='avatars/', verbose_name=_('Avatar'), blank=True, null=True)

	def __str__(self):
		return self.user.username
