from django import forms
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth  import settings

''' 
Two kinds of article
'''
#blog is a list for articles
class Article(models.Model):
    title = models.CharField(max_length=50)
    time = models.DateTimeField()
    content = RichTextField()

    class Meta:
        abstract = 'True'
        ordering = ('-time',)

#dairy is used for time line
class Diary(Article):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    class Meta:
        db_table = 'diary'

class Blog(Article):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    class Meta:
        db_table = 'blog'

'''
Form to post new article
'''
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title','content')

class UserExtra(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extension')
    pic = models.ImageField(upload_to='user_image', default = 'user_image/None/no-img.jpg')
    motto = models.CharField(max_length=200, default= 'Motto')
    class Meta:
        db_table = 'UserExtra'


@receiver(post_save,sender=User)
def create_user_extension(sender,instance,created,**kwargs):
    if created:
        UserExtra.objects.create(user=instance)
    else:
        instance.extension.save()


