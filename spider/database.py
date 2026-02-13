import pymysql
from config import DB_CONFIG
from contextlib import contextmanager

class Database:
    def __init__(self):
        self.config = DB_CONFIG
    
    @contextmanager
    def get_connection(self):
        conn = pymysql.connect(**self.config)
        try:
            yield conn
        finally:
            conn.close()
    
    @contextmanager
    def get_cursor(self):
        with self.get_connection() as conn:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
    
    def execute(self, sql, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount
    
    def fetchall(self, sql, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    
    def fetchone(self, sql, params=None):
        with self.get_cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()
    
    def insert_many(self, sql, params_list):
        with self.get_cursor() as cursor:
            cursor.executemany(sql, params_list)
            return cursor.rowcount

db = Database()
