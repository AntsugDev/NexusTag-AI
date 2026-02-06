import sqlite3
import os
import sqlite_vec
class ConnectionSqlite:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'rag.db'))
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

    def migration(self):
        try:
            if(os.path.exists(os.path.join(os.path.dirname(__file__), 'schema.sql'))):
                with open(os.path.join(os.path.dirname(__file__), 'schema.sql'), 'r') as f:
                    self.cursor.executescript(f.read())   
            else:
                raise Exception("schema.sql not found") 
        except Exception as e:
            raise e    

    def close(self):
        self.conn.close() 

if __name__ == "__main__":
    conn = ConnectionSqlite()
    conn.migration()
    conn.close()
