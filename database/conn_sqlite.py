import sqlite3
import os
import sqlite_vec

class ConnectionSqlite:
    def __init__(self):
        self.conn = sqlite3.connect('nexus-tag-ai.db')
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
                if not os.path.exists('nexus-tag-ai.db') :
                    self.cursor = self.getCursor()
                    self.cursor.executescript(readFile.read())  
                    self.cursor.connection.commit() 
                else :
                    print(f"esiste, ma lo forzo ? {'SI' if is_force > 0 else 'NO'}")
                    if is_force > 0:
                        self.cursor = self.getCursor()
                        self.cursor.executescript(readFile.read())  
                        self.cursor.connection.commit() 
                    else:    
                        print("Database already exists ...")    
            else:
                raise Exception("schema.sql not found") 
        except Exception as e:
            raise e    

    def close(self):
        self.conn.close() 

if __name__ == "__main__":
    conn = ConnectionSqlite()
    conn.migration(is_force=1)
    conn.close()
