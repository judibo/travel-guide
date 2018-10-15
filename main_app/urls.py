from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('user/<username>', views.profile, name='profile'),
    path('city/', views.spots_index, name='spots_index'),
    path('spot/create', views.SpotCreate.as_view(), name='spots_create'),
    path('city/<int:spot_id>', views.spots_detail, name='spots_detail'),
    path('bucketlist/<int:bucketlist_id>', views.bucketlist, name='bucketlist'),
]