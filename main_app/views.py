from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import LoginForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Spot, City, Bucketlist, BucketSpot, Comment, Photo
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import uuid
import boto3

# Constants
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'wherenext'

# Create your views here.
def index(request):
  return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data['username']
            p = form.cleaned_data['password']
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    print("The account has been disabled.")
                    return HttpResponseRedirect('/')
            else:
                print("The username and/or password is incorrect.")
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})

def city_index(request):
    cities = City.objects.all()
    return render(request, 'city/index.html', {'cities': cities})

def city_detail(request, city_id):
    city = City.objects.get(id=city_id)
    spots = Spot.objects.filter(bucketspot__bucket__city=city).values('id', 'name', 'details', 'genre').distinct()
    return render(request, 'city/detail.html', {'city': city, 'spots': spots})

@login_required
def spots_detail(request, spot_id):
    spot = Spot.objects.get(id=spot_id)
    bucketspot = BucketSpot.objects.filter(bucket__user=request.user, spot=spot).first()
    comment_form = CommentForm()
    city = spot.bucketspot_set.first().bucket.city.name
    return render(request, 'city/spot.html', {'spot': spot, 'city': city, 'bucketspot': bucketspot, 'comment_form': comment_form, 'current_user': request.user})

def bucketlist(request, bucketlist_id):
    bucketlist = Bucketlist.objects.get(id=bucketlist_id)
    return render(request, 'bucketlist.html', {'bucketlist': bucketlist })

def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile.html')

@method_decorator(login_required, name='dispatch')
class SpotCreate(CreateView):
    model = Spot
    fields = '__all__'
    def form_valid(self, form, *args, **kwargs):
        self.object = form.save()
        bucketlist = Bucketlist.objects.filter(user=self.request.user, city_id=self.kwargs['pk'])
        if len(bucketlist):
            bucketlist = bucketlist[0]
        else:
            bucketlist = Bucketlist(city_id=self.kwargs['pk'], user=self.request.user)
            bucketlist.save()
        bs = BucketSpot(bucket=bucketlist, spot=self.object) 
        bs.save()
        photo_file = self.request.FILES.get('photo-file', None)
        if photo_file:
            s3 = boto3.client('s3')
            key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
            try:
                s3.upload_fileobj(photo_file, BUCKET, key)
                url = f"{S3_BASE_URL}{BUCKET}/{key}"
                photo = Photo(url=url, spot=self.object)
                photo.save()
            except:
                print('An error occurred uploading file to S3')
        return redirect(f"/city/{self.kwargs['pk']}")

def add_spot_bucket(request, spot_id):
    spot = Spot.objects.get(id=spot_id)
    city = spot.bucketspot_set.first().bucket.city
    bucketlist, created = Bucketlist.objects.get_or_create(user=request.user, city=city)
    bucketspot = BucketSpot(bucket=bucketlist, spot=spot)
    bucketspot.save()
    return redirect(f"/bucketlist/{bucketlist.id}")

def check_done(request, bucketspot_id):
    bs = BucketSpot.objects.get(id=bucketspot_id)
    bs.done = True
    bs.save()
    return redirect('spots_detail', spot_id=bs.spot.id)

@method_decorator(login_required, name='dispatch')
class CityCreate(CreateView):
    model = City
    fields = '__all__'
    success_url = '/city'
   
def add_comment(request, spot_id):
   form = CommentForm(request.POST)
   if form.is_valid():
       new_comment = form.save(commit=False)
       new_comment.user = request.user
       new_comment.spot_id = spot_id
       new_comment.save()
   return redirect('spots_detail', spot_id=spot_id)

class CommentUpdate(UpdateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return redirect(f"/spot/{self.object.spot_id}")

class CommentDelete(DeleteView):
   model = Comment
   def post(self, request, *args, **kwargs):
       comment = self.get_object()
       spot_id = comment.spot_id
       comment.delete()
       return redirect(f"/spot/{spot_id}")

def add_photo(request, spot_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, spot_id=spot_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('spots_detail', spot_id=spot_id)
