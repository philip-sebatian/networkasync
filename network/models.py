from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers=models.ManyToManyField('self',symmetrical=False,blank=True,related_name='flr')
    following=models.ManyToManyField('self',symmetrical=False,blank=True,related_name='fly')

class Post(models.Model):
    content=models.CharField(max_length=1000)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    liked_by=models.ManyToManyField(User,symmetrical=False,related_name="liked_by",blank=True)
