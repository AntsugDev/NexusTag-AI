import sqlite3
import os
import sqlite_vec
from datetime import datetime

class ConnectionSqlite:
    def __init__(self):
        self.database = os.path.join(os.path.dirname(__file__), 'nexus-tag-ai.sqlite')
        self.conn = sqlite3.connect(self.database,check_same_thread=False)
        self.conn.enable_load_extension(True)
        sqlite_vec.load(self.conn)
        self.cursor = None

    def get_connection(self, row_factory=False):
        """Ottieni o crea una connessione"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
        
        if row_factory:
            self.conn.row_factory = sqlite3.Row
        else:
            self.conn.row_factory = None  # Reset se non serve
            
        return self.conn
    
    def getCursor(self, row_factory=False):
        """Ottieni un cursor con opzionale row_factory"""
        conn = self.get_connection(row_factory)
        return conn.cursor()

    def migration(self, is_force=0):
        try:
            readFile = None
            if(os.path.exists(os.path.join(os.path.dirname(__file__), 'schema.sql'))):
                readFile = open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r')
                if not os.path.exists(self.database) :
                    self.cursor = self.getCursor()
                    self.cursor.executescript(readFile.read())  
                    self.cursor.connection.commit() 
                else :
                    print(f"esiste, ma lo forzo ? {'SI' if is_force > 0 else 'NO'}")
                    if is_force > 0:
                        self.cursor = self.getCursor()
                        self.cursor.executescript(readFile.read())  
                        self.cursor.connection.commit() 
                        self.seeders()
                    else:    
                        print("Database already exists ...")    
            else:
                raise Exception("schema.sql not found") 
        except Exception as e:
            raise e 

    def seeders(self):
        try:
            status_files = [
                {'label': 'pending', 'created_at': datetime.now()},
                {'label': 'processing', 'created_at': datetime.now()},
                {'label': 'completed', 'created_at': datetime.now()},
                {'label': 'failed', 'created_at': datetime.now()},
                {'label': 'uploaded', 'created_at': datetime.now()}
            ]
            self.cursor = self.getCursor()
            for status_file in status_files:
                self.cursor.execute('INSERT INTO STATUS_FILES (label, created_at) VALUES (?, ?)', (status_file['label'], status_file['created_at']))
            self.cursor.connection.commit() 

            strategy_chunks = [
                {'label': 'recursive', 'created_at': datetime.now()},
                {'label': 'markdown_and_recursive', 'created_at': datetime.now()},
                {'label': 'markdown', 'created_at': datetime.now()},
                {'label': 'excel', 'created_at': datetime.now()},
                {'label': 'database', 'created_at': datetime.now()},
                {'label': 'json', 'created_at': datetime.now()},
                {'label': 'code_language', 'created_at': datetime.now()},
                {'label': 'generic', 'created_at': datetime.now()}
            ]
            self.cursor = self.getCursor()
            for strategy_chunk in strategy_chunks:
                self.cursor.execute('INSERT INTO STRATEGY_CHUNKS (label, created_at) VALUES (?, ?)', (strategy_chunk['label'], strategy_chunk['created_at']))
            self.cursor.connection.commit() 
        except Exception as e:
            raise e         

    def close(self):
        self.conn.close() 
