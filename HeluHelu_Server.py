import sqlite3
import Crypto.Random
import Crypto.Protocol.KDF
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

def add_user(conn, username, password):
    curs = conn.cursor()
    salt = Crypto.Random.get_random_bytes(8)
    hash = Crypto.Protocol.KDF.PBKDF2(password, salt)
    print('\nADDING...')
    print(username)
    print(salt.hex())
    print(hash.hex())
    curs.execute('INSERT INTO users VALUES (?,?,?,?,?)',
                (username, salt.hex(), hash.hex(), ' ', ' '))
    conn.commit()

def authenticate_user(conn, username, password):
    curs = conn.cursor()
    results = curs.execute('SELECT salt, hash FROM users WHERE username=?',
                          (username,))
    row = results.fetchone()
    salt = bytes.fromhex(row[0])
    hash = bytes.fromhex(row[1])
    if hash == Crypto.Protocol.KDF.PBKDF2(password, salt):
        return True
    else:
        return False

def get_books(conn, username):
    curs = conn.cursor()
    results = curs.execute(
               'SELECT books FROM users WHERE username=?',
               (username,))
    return results.fetchone()[0].split(';')

def get_favorites(curs, username):
    curs = conn.cursor()
    results = curs.execute(
               'SELECT favorites FROM users WHERE username=?',
               (username,))
    return results.fetchone()[0].split(';')

def search_books(api_key, keywords, cache):
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

def add_book(conn, username, book):
    curs = conn.cursor()
    results = curs.execute(
               'SELECT books FROM users WHERE username=?',
               (username,))
    old_list = results.fetchone()[0]
    new_list = book.title + ';' + old_list
    curs.execute('UPDATE users SET books=? WHERE username=?',
                (new_list, username))
    book_count = curs.execute(
                 'SELECT count FROM books WHERE book_id=?',
                 (book.book_id,)).fetchone()
    if book_count:
        curs.execute('UPDATE books SET count=? WHERE book_id=?',
                (book_count[0] + 1, book.book_id))
    else:
        curs.execute(
               '''INSERT INTO books VALUES (?,?,?,?,?,?,?)''',
               (book.book_id, book.title, book.author,
               book.year, book.image, 1, 0))
    conn.commit()

# MAIN
api_key = open('api_key.txt', 'r').read()[:-1]
Crypto.Random.new()
db = input('enter database filename: ')
conn = sqlite3.connect(db)
cache = Cache()
