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
