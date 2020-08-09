from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from backend.models import Book
from backend.forms import SearchForm, AddBooksForm
import urllib.request
import xml.etree.ElementTree

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
        existing_session_cache = False
        if form.is_valid():
            keywords = form.cleaned_data['keywords']
            try: # see if there's a session cache
                cache = request.session['cache']
                existing_session_cache = True
                if keywords in cache: # see if it contains this query
                    context = {'results_list': cache[keywords],}
                    return render(request, 'results.html', context)
            except: # there's no session cache
                pass   
            # or the query isn't cached, so continue here
            api_key = open('api_key.txt', 'r').read()[:-1]
            prefix = 'https://www.goodreads.com/search.xml?key='
            url_keywords = keywords.replace(' ', '+')
            with urllib.request.urlopen(prefix +
                                        api_key +
                                        '&q=' +
                                        url_keywords) as response:
               results_root = xml.etree.ElementTree.fromstring(response.read())
            # this list stores books extracted from the API response
            results = []
            for work in results_root[1][6]:
                # create a dictionary for each book
                book = {}
                book['book_id'] = work[0].text
                book['title'] = work[8][1].text
                book['author'] = work[8][2][1].text
                book['year'] = work[4].text
                book['image'] = work[8][3].text
                results.append(book)
            if not existing_session_cache:
                cache = {}
            # cache the results of this query in case the user repeats it,
            # and to facilitate their selections in the next step
            cache[keywords] = results[:5]
            request.session['cache'] = cache
            add_books_form = AddBooksForm()
            zipped_lists = zip(add_books_form, results[:10])
            context = {'zipped_lists': zipped_lists, 'keywords': keywords}
            return render(request, 'results.html', context)
        else:
            return HttpResponseRedirect(reverse('search')) 
    else: # request.method == 'GET'
        form = SearchForm()
        context = {'form': form,}
        return render(request, 'search.html', context)
