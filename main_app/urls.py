from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('user/<username>/', views.profile, name='profile'),
    path('city/', views.city_index, name='city_index'),
    path('city/<int:city_id>/', views.city_detail, name='city_detail'),
    path('city/add_city/', views.CityCreate.as_view(), name='add_city'),
    path('city/<int:pk>/add_spot/', views.SpotCreate.as_view(), name='add_spot'),
    path('spot/<int:spot_id>/', views.spots_detail, name='spots_detail'),
    path('spot/<int:spot_id>/add_comment/', views.add_comment, name='add_comment'),
    path('spot/<int:pk>/update/', views.CommentUpdate.as_view(), name='comment_update'),
    path('spot/<int:pk>/delete/', views.CommentDelete.as_view(), name='comment_delete'),
    path('spot/<int:spot_id>/add', views.add_spot_bucket, name='add_spot_bucket'),
    path('bucketlist/<int:bucketlist_id>/', views.bucketlist, name='bucketlist'),
]