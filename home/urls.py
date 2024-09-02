from django.urls import path
from home import views

urlpatterns = [
    path('', views.sign_up, name='home-url'),
    path('Signin/', views.sign_in, name='sign-in-url'),
    path('Signup/', views.sign_up, name='sign-up-url'),
    path('Signout/', views.sign_out, name='signout-url'),
    path('Search/', views.search, name='search-url')
]

