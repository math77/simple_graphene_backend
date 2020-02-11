from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Actor(models.Model):
    name = models.CharField(max_length=100)
    photo_url = models.ImageField(upload_to='actors_photos/')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    year = models.IntegerField()
    actors = models.ManyToManyField(Actor)
    duration_in_minutes = models.IntegerField()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=210)
    created = models.DateTimeField(null=False, auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('created',)


class Watched(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_in = models.DateTimeField(null=False, auto_now_add=True)
    favorite = models.BooleanField(default=False, null=True)
    vote = models.IntegerField()

    def __str__(self):
        return self.movie.title

    class Meta:
        ordering = ('vote',)
