from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Song(models.Model):
    song_name = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    likers = models.ManyToManyField(User, related_name='liked_songs')
    song_cover = models.ImageField(blank=True, null=True)
    fans = models.ManyToManyField(User, related_name='fav_songs')

    def __str__(self) :
        return self.song_name


class User_prof(models.Model):
    common_users = models.ManyToManyField(User)


class ListCat(models.Model):
    name = models.CharField(max_length=15, unique=True, primary_key=True)


class List(models.Model):
    name = models.CharField(max_length=50)
    categories = models.ManyToManyField(ListCat)
    songs = models.ManyToManyField(Song)
    auther = models.ForeignKey(User, on_delete=models.CASCADE)
   
   

    def __str__(self) : 
        return self.name


class Feedback(models.Model):
    feddback_text = models.CharField(max_length=3000)
