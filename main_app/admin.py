from django.contrib import admin
from .models import Spot, City, Bucketlist, BucketSpot, Comment, Photo

# Register your models here.

admin.site.register(Spot)
admin.site.register(City)
admin.site.register(BucketSpot)
admin.site.register(Bucketlist)
admin.site.register(Comment)
admin.site.register(Photo)