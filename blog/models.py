from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
	"""Post model."""
	title = models.CharField(max_length=225)
	text = models.TextField()
	reg_date = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post', default='1')
	members = models.ManyToManyField(User, related_name='members', blank=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'post'
		verbose_name_plural = 'posts'
		ordering = ['-reg_date']
