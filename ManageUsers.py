import sqlite3
import Crypto.Random
import Crypto.Protocol.KDF

def add_user(curs, username, password):
    salt = Crypto.Random.get_random_bytes(8)
    hash = Crypto.Protocol.KDF.PBKDF2(password, salt)
    print('\nADDING...')
    print(username)
    print(salt.hex())
    print(hash.hex())
    curs.execute('INSERT INTO users VALUES (?,?,?)',
                (username, salt.hex(), hash.hex()))

def authenticate_user(curs, username, password):
    results = curs.execute('SELECT salt, hash FROM users WHERE username=?',
                          (username,))
    row = results.fetchone()
    salt = bytes.fromhex(row[0])
    hash = bytes.fromhex(row[1])
    if hash == Crypto.Protocol.KDF.PBKDF2(password, salt):
        return True
    else:
        return False

Crypto.Random.new()
conn = sqlite3.connect('test0.db')
curs = conn.cursor()

try:
    username = input('enter new username: ')
    password = input('enter new password: ')
    add_user(curs, username, password)
    print('SUCCESS\n')
    conn.commit()
except:
    print('FAILED\n')
    conn.rollback()

try:
    username = input('enter existing username: ')
    password = input('enter existing password: ')
    if authenticate_user(curs, username, password):
        print('VALID\n')
    else:
        print('NOT VALID\n')
except:
    print('FAILED\n')

conn.close()
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
