from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('community', views.community, name='community'),
    path('books', views.books, name='books'),
    path('search', views.search, name='search'),
    path('results', views.results, name='results'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
