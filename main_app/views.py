from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import LoginForm, CommentForm, CheckDone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Spot, City, Bucketlist, BucketSpot, Comment
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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

def spots_detail(request, spot_id):
    spot = Spot.objects.get(id=spot_id)
    bucketspots = spot.bucketspot_set.all()
    comment_form = CommentForm()
    city = spot.bucketspot_set.first().bucket.city.name 
    return render(request, 'city/spot.html', {'spot': spot, 'city': city, 'bucketspots': bucketspots, 'comment_form': comment_form, 'current_user': request.user})

def bucketlist(request, bucketlist_id):
    bucketlist = Bucketlist.objects.get(id=bucketlist_id)
    return render(request, 'bucketlist.html', {'bucketlist': bucketlist })

def profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile.html')

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
        return redirect(f"/city/{self.kwargs['pk']}")

def add_spot_bucket(request, spot_id):
    spot = Spot.objects.get(id=spot_id)
    city = spot.bucketspot_set.first().bucket.city
    bucketlist, created = Bucketlist.objects.get_or_create(user=request.user, city=city)
    bucketspot = BucketSpot(bucket=bucketlist, spot=spot)
    bucketspot.save()
    return redirect(f"/bucketlist/{bucketlist.id}")

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


def check_done(request, spot_id):
    if request.method == 'POST':
        form = CheckDone(request.POST)
        if form.is_valid():
            result = "valid"
        else:
            result = "not valid"
    else:
        form = CheckDone()
        result = "no post"
    return redirect('spots_detail', spot_id=spot_id)
