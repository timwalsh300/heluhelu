from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.community, name='community'),
    path('', views.books, name='books'),
    path('search', views.search, name='search'),
]
