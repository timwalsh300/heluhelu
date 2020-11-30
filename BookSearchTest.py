import urllib.request
import xml.etree.ElementTree

class Book():
    pass

class Cache():
    cache = {}
    def add(self, keywords, results_list):
        self.cache[keywords] = results_list
    def check(self, keywords):
        if keywords in self.cache:
            return self.cache[keywords]
        else:
            return None

def get_results(api_key, keywords, cache):
    cached_results = cache.check(keywords)
    if cached_results:
        return cached_results
    else:
        prefix = 'https://www.goodreads.com/search.xml?key='
        url_keywords = keywords.replace(' ', '+')
        with urllib.request.urlopen(prefix +
                                    api_key +
                                    '&q=' +
                                    url_keywords) as response:
            results_root = xml.etree.ElementTree.fromstring(response.read())
        results_list = []
        for work in results_root[1][6]:
            book = Book()
            book.book_id = work[0].text
            book.title = work[8][1].text
            book.author = work[8][2][1].text
            book.year = work[4].text
            book.image = work[8][3].text
            results_list.append(book)
        cache.add(keywords, results_list[:5])
        return results_list[:5]

cache = Cache()
api_key = open('api_key.txt', 'r').read()[:-1]
while True:
    query = input('\nsearch for: ')
    i = 1
    for book in get_results(api_key, query, cache):
        print(str(i) + ' ' + book.title)
        i += 1
