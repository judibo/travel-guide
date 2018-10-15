from django.db import models
from django.contrib.auth.models import User

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    currency = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Bucketlist(models.Model): 
    created_at = models.DateField(auto_now_add=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Spot(models.Model):
    GENRES = (
        (1, 'Tourist Spot'),
        (2, 'Restaurant'),
        (3, 'Bar'),
    )
    name = models.CharField(max_length=100)
    details = models.TextField(max_length=1000)
    genre = models.IntegerField(
        choices=GENRES,
        default=GENRES[0][0]
    )
    def __str__(self):
        return self.name

class BucketSpot(models.Model):
    bucket = models.ForeignKey(Bucketlist, on_delete=models.CASCADE)
    spot = models.ForeignKey(Spot, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)