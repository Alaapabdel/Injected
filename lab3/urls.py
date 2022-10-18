from django.urls import path
from . import views

app_name = "lab3"
urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('admin', views.admin, name='admin'),
    path('details', views.details, name='details'),
    path('credentials', views.credentials, name='credentials'),
    path('search', views.search, name='search'),
    path('succeed', views.succeed, name='succeed'),
]
