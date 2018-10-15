from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Spot, City, Bucketlist, BucketSpot
from django.views.generic.edit import CreateView

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
    spots = Spot.objects.all()
    return render(request, 'city/detail.html', {'spots': spots}, {'city': city})

def spots_detail(request, spot_id):
    spot = Spot.objects.get(id=spot_id)
    bucketspots = spot.bucketspot_set.all()
    city = spot.bucketspot_set.first().bucket.city.name 
    return render(request, 'city/spot.html', {'spot': spot, 'city': city, 'bucketspots': bucketspots})

def bucketlist(request, bucketlist_id):
    bucket = Bucketlist.objects.get(id=bucketlist_id)
    city = City.objects.all()
    return render(request, 'bucketlist.html', {'bucket': bucket}, {'city': city})

def profile(request, username):
    user = User.objects.get(username=username)
    bucketlists = Bucketlist.objects.filter(user=user)
    return render(request, 'profile.html',{'username': username}, {'bucketlists': bucketlists})

class SpotCreate(CreateView):
    model = Spot
    fields = '__all__'
    success_url = '/city'