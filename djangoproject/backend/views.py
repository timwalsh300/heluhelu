from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F
from backend.models import Book
from backend.forms import SearchForm, AddBooksForm, CreateForm
import urllib.request
import xml.etree.ElementTree
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    num_users = User.objects.all().count()
    num_books = Book.objects.filter(num_owners__gt=0).count()
    most_popular = Book.objects.order_by('num_owners').reverse()[:5]
    context = {'num_users': num_users, 'num_books': num_books, 'most_popular': most_popular}
    return render(request, 'index.html', context)

def create_account_view(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            try:
                existing_user = User.objects.get(username=username)
                # username is already taken, try again
                form = CreateForm()
                context = {'form': form,}
                return render(request, 'create.html', context)
            except User.DoesNotExist:
                # username is available; now check that passwords match
                if password1 == password2:
                    user = User.objects.create_user(username, email, password1)
                    user.save()
                    return HttpResponseRedirect(reverse('login')) 
                else:
                    form = CreateForm()
                    context = {'form': form,}
                    return render(request, 'create.html', context)
        else:
            form = CreateForm()
            context = {'form': form,}
            return render(request, 'create.html', context)
    else: # request.method == 'GET'
        form = CreateForm()
        context = {'form': form,}
        return render(request, 'create.html', context)
    

class UserListView(generic.ListView):
    model = User

def user_detail_view(request, u):
    try:
        user = User.objects.get(username=u)
        books = Book.objects.filter(owners=user)
    except User.DoesNotExist:
        raise Http404('User does not exist')
    # must use 'user_obj' here instead of 'user' because that is reserved
    # in the template language for the logged in user    
    return render(request, 'auth/user_detail.html', context={'user_obj': user, 'books': books})

@login_required
def remove_book(request, book_id):    
    selection = Book.objects.get(goodreads_id=book_id)
    selection.owners.remove(request.user)
    selection.num_owners = F('num_owners') - 1
    selection.save()
    books = Book.objects.filter(owners=request.user)
    context = {'books': books,}
    return render(request, 'books.html', context)

@login_required
def add_book(request, book_id):    
    selection = Book.objects.get(goodreads_id=book_id)
    selection.owners.add(request.user)
    selection.num_owners = F('num_owners') + 1
    selection.save()
    books = Book.objects.filter(owners=request.user)
    context = {'books': books,}
    return render(request, 'books.html', context)

@login_required
def books(request):
    books = Book.objects.filter(owners=request.user)
    context = {'books': books,}
    return render(request, 'books.html', context)

@login_required
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        existing_session_cache = False
        add_books_form = AddBooksForm()
        if form.is_valid():
            keywords = form.cleaned_data['keywords']
            try: # see if there's a session cache
                cache = request.session['cache']
                existing_session_cache = True
                if keywords in cache: # see if it contains this query
                    zipped_lists = zip(add_books_form, cache[keywords])
                    context = {'zipped_lists': zipped_lists,
                               'keywords': keywords}
                    return render(request, 'results.html', context)
            except: # there's no session cache
                pass   
            # or the query isn't cached, so continue here
            api_key = open('/home/tim/heluhelu/djangoproject/backend/api_key.txt', 'r').read()[:-1]
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
                book['goodreads_id'] = work[0].text
                book['title'] = work[8][1].text
                book['author'] = work[8][2][1].text
                book['year'] = work[4].text
                book['image'] = work[8][3].text
                results.append(book)
            if not existing_session_cache:
                cache = {}
            # cache the results of this query in case the user repeats it,
            # and to facilitate their selections in the next step
            cache[keywords] = results[:10]
            request.session['cache'] = cache
            zipped_lists = zip(add_books_form, results[:10])
            context = {'zipped_lists': zipped_lists, 'keywords': keywords}
            return render(request, 'results.html', context)
        else:
            return HttpResponseRedirect(reverse('search')) 
    else: # request.method == 'GET'
        form = SearchForm()
        context = {'form': form,}
        return render(request, 'search.html', context)

@login_required
def results(request):
    if request.method == 'POST':
        cached_results = request.session['cache'][request.POST['keywords']]
        for i in range(0,10):
            choice = 'select_result_' + str(i)
            if choice in request.POST:
              try:
                selection = Book.objects.get(goodreads_id=cached_results[i]['goodreads_id'])
              except Book.DoesNotExist:
                book = Book()
                book.goodreads_id = cached_results[i]['goodreads_id']
                book.title = cached_results[i]['title']
                book.author = cached_results[i]['author']
                book.year = cached_results[i]['year']
                book.image = cached_results[i]['image']
                book.save()
              finally:
                selection = Book.objects.get(goodreads_id=cached_results[i]['goodreads_id'])
                selection.num_owners = F('num_owners') + 1
                selection.owners.add(request.user)
                selection.save()
        return HttpResponseRedirect(reverse('index')) 
    else: # request.method == 'GET'
        form = SearchForm()
        context = {'form': form,}
        return render(request, 'search.html', context)

