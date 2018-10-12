from django.contrib import admin
from .models import Spot, City, Bucketlist

# Register your models here.

admin.site.register(Spot)
admin.site.register(City)
admin.site.register(Bucketlist)