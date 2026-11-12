from pathlib import Path
from contextlib import contextmanager
import os,sqlite3
DB_PATH=Path(os.environ.get('BOOKS_DB',Path(__file__).with_name('data.db')))
@contextmanager
def create_connection():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()
def create_db_table():
    with create_connection() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS books (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          author TEXT NOT NULL,
          year INTEGER NOT NULL CHECK(year BETWEEN 1450 AND 2100),
          genre TEXT NOT NULL,
          status TEXT NOT NULL DEFAULT 'Не прочитано'
        )''')
def insert_item(data):
    with create_connection() as conn:
        cur=conn.execute('INSERT INTO books(title,author,year,genre,status) VALUES(?,?,?,?,?)',data)
        return cur.lastrowid
def get_all_items():
    with create_connection() as conn:
        return conn.execute('SELECT * FROM books ORDER BY id').fetchall()
def get_item_by_id(item_id):
    with create_connection() as conn:
        return conn.execute('SELECT * FROM books WHERE id=?',(item_id,)).fetchone()
def update_item(item_id,new_data):
    with create_connection() as conn:
        return conn.execute('UPDATE books SET title=?,author=?,year=?,genre=?,status=? WHERE id=?',(*new_data,item_id)).rowcount
def delete_item(item_id):
    with create_connection() as conn:
        return conn.execute('DELETE FROM books WHERE id=?',(item_id,)).rowcount
