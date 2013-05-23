import sqlite3
import utility

#con = None
#con = sqlite3.connect(utility.DB_NAME)
#con = sqlite3.connect(utility.DB_NAME, check_same_thread=False)

class Db():
    
    def __init__(self):
        self.init_table()
    
    def init_table(self):
        con = None
        con = sqlite3.connect(utility.DB_NAME)

        with con:
            cur = con.cursor()
            
            cur.execute("CREATE TABLE IF NOT EXISTS Parameter(key TEXT PRIMARY KEY ASC, value TEXT)")
            cur.execute("CREATE TABLE IF NOT EXISTS Monitor(symbol TEXT PRIMARY KEY ASC)")
            cur.execute("CREATE TABLE IF NOT EXISTS Alert(symbol TEXT, cross TEXT, level NUMERIC, price_last_refresh NUMERIC, PRIMARY KEY (symbol, cross, level))")
    
    def get_table_content(self, table):
        con = None
        con = sqlite3.connect(utility.DB_NAME)
        
        with con:
            return self.select_query("SELECT * FROM " + table)
    
    
    def exec_query(self, query):
        con = None
        con = sqlite3.connect(utility.DB_NAME)
        
        with con:
            cur = con.cursor()
            cur.execute(query)
            return None
    
    def select_query(self, query):
        con = None
        con = sqlite3.connect(utility.DB_NAME)

        with con:
            cur = con.cursor()    
            cur.execute(query)
            return cur.fetchall()
    
    def insert_query(self, table, data):
        
        vec_value = "("
        for entry in data[0]:
            vec_value += "?,"
        vec_value =vec_value[:-1] + ")"
        
        con = None
        con = sqlite3.connect(utility.DB_NAME)
        
        with con:
            cur = con.cursor()
            cur.executemany("INSERT INTO " + table + " VALUES" + vec_value, data)
        