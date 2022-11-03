
from django.db import models

# Create your models here.
class Artiste(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField(null=True)

    def __str__(self):
        return self.first_name

class Song(models.Model):
    title = models.CharField(max_length=200)
    date_released = models.DateField(null=True, blank=True)
    likes = models.IntegerField(null=True)
    artiste = models.ForeignKey('Artiste', on_delete = models.CASCADE)

    def __str__(self):
        return self.title

class Lyric(models.Model):
    content = models.CharField(max_length=1000)
    song = models.ForeignKey('Song', on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.song, self.song.artiste)
