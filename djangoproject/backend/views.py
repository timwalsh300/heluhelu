from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from backend.models import Book
from backend.forms import SearchForm
import urllib.request
import xml.etree.ElementTree

class BookObject():
    pass

# Create your views here.
def index(request):
    num_users = User.objects.all().count()
    num_books = Book.objects.all().count()
    context = {'num_users': num_users, 'num_books': num_books,}
    return render(request, 'index.html', context=context)

def community(request):
    num_users = User.objects.all().count()
    num_books = Book.objects.all().count()
    context = {'num_users': num_users, 'num_books': num_books,}
    return render(request, 'community.html', context=context)

def books(request):
    num_users = User.objects.all().count()
    num_books = Book.objects.all().count()
    context = {'num_users': num_users, 'num_books': num_books,}
    return render(request, 'users.html', context=context)

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            keywords = form.cleaned_data['keywords']
            api_key = open('api_key.txt', 'r').read()[:-1]
            prefix = 'https://www.goodreads.com/search.xml?key='
            url_keywords = keywords.replace(' ', '+')
            with urllib.request.urlopen(prefix +
                                        api_key +
                                        '&q=' +
                                        url_keywords) as response:
                    results_root = xml.etree.ElementTree.fromstring(response.read())
            results_list = []
            for work in results_root[1][6]:
                book = BookObject()
                book.book_id = work[0].text
                book.title = work[8][1].text
                book.author = work[8][2][1].text
                book.year = work[4].text
                book.image = work[8][3].text
                results_list.append(book)
            context = {'results_list': results_list,}
            return render(request, 'results.html', context)
        else:
            return HttpResponseRedirect(reverse('search')) 
    else: # request.method == 'GET'
        form = SearchForm()
        context = {'form': form,}
        return render(request, 'search.html', context)
