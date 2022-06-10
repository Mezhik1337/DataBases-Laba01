from django.urls import path

from . import views
from .static import images

urlpatterns = [
    path('', views.index, name= 'home'),
    path('about', views.about , name='about'),
    path('city', views.city, name ='city'),
    path('sportsman', views.sportsman, name ='sportsman'),
    path('create', views.create, name ='create' ),
    path('request', views.request, name ='request'),
    path('request1', views.request1, name ='request1'),
    path('request2', views.request2, name ='request2'),
    path('request3', views.request3, name ='request3'),
    path('request4', views.request4, name ='request4')
]
