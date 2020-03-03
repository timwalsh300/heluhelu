import sqlite3

name = input('enter name of new heluhelu database: ')
try:
    conn = sqlite3.connect(name)
    curs = conn.cursor()
    curs.execute('''CREATE TABLE users
                 (username text, salt text, hash text,
                 PRIMARY KEY (username))''')
    curs.execute('''CREATE TABLE books
                 (book_id text, title text, author text, year text,
                 image text, count integer, favorite_count integer,
                 PRIMARY KEY (book_id))''')
    curs.execute('''CREATE TABLE user_data
                 (username text, book_list text, favorite_list text,
                 PRIMARY KEY (username))''')
    conn.commit()
    print('success')
except:
    print('failed to create database')
finally:
    conn.close()
