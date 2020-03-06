import sqlite3

name = input('enter name of new heluhelu database: ')
try:
    conn = sqlite3.connect(name)
    curs = conn.cursor()
    curs.execute('''CREATE TABLE users
                 (username text, salt text, hash text, books blob,
                 favorites text, PRIMARY KEY (username))''')
    curs.execute('''CREATE TABLE books
                 (book_id text, title text, author text, year text,
                 image blob, count integer, favorite_count integer,
                 PRIMARY KEY (book_id))''')
    conn.commit()
    print('success')
except:
    print('failed to create database')
finally:
    conn.close()
