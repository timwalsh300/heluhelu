from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.create_account_view, name='create'),
    path('community', views.UserListView.as_view(), name='community'),
    path('user/<u>', views.user_detail_view, name='user-detail'),
    path('books', views.books, name='books'),
    path('search', views.search, name='search'),
    path('results', views.results, name='results'),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
