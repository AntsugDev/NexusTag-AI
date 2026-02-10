import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.conn_sqlite import ConnectionSqlite
from utility.utility import ExceptionRequest
class ModelGeneral():
    def __init__(self,db_connection=None):
        self.table = None
        self.data = {}
        self._conn = db_connection or ConnectionSqlite()

    def insert(self, data):
        """Inserisce un nuovo record e restituisce l'ID"""
        s = f"""INSERT INTO {self.table} ({', '.join(data.keys())}) VALUES ({', '.join(['?' for _ in data.values()])})"""
        return  self.execute(s, tuple(data.values()))
    
    def get_last_insert_id(self):
        """Restituisce l'ultimo record inserito basandosi su rowid"""
        s = f"SELECT * FROM {self.table} WHERE rowid = last_insert_rowid()"
        result = self.execute(s, fetch=True)
        return result[0] if result else None
    
    def update(self, data, where_id):
        """Aggiorna un record esistente"""
        s = f"""UPDATE {self.table} SET {', '.join([f'{key} = ?' for key in data.keys()])} WHERE id = ?"""
        values = list(data.values()) + [where_id]
        self.execute(s, tuple(values))
        return True
    
    def delete(self, id):
        """Elimina un record"""
        s = f"""DELETE FROM {self.table} WHERE id = ?"""
        self.execute(s, (id,))
        return True

    def show(self, id, columns=None):
        """Mostra un singolo record"""
        s = f"""SELECT {','.join(columns) if columns is not None else '*'} FROM {self.table} WHERE id = ?"""
        return self.execute(s, (id,), one=True)

    def global_search(self, columns=None):
        """Restituisce tutti i record"""
        s = f"""SELECT {','.join(columns) if columns is not None else '*'} FROM {self.table}"""
        return self.execute(s, fetch=True)

    def search(self, data):
        """Cerca record con criteri specifici"""
        s = f"""SELECT * FROM {self.table} WHERE {' AND '.join([f'{key} = ?' for key in data.keys()])}"""
        return self.execute(s, tuple(data.values()), fetch=True)        
    
    def paginate(self, page=1, limit=10, data=None):
        """Restituisce record paginati"""
        offset = (page - 1) * limit
        where_clause = ""
        values = []
        if data:
            where_clause = f" WHERE {' AND '.join([f'{key} = ?' for key in data.keys()])}"
            values = list(data.values())
        
        s = f"SELECT * FROM {self.table}{where_clause} LIMIT ? OFFSET ?"
        values.extend([limit, offset])
        return self.execute(s, tuple(values), fetch=True)
    
    def count(self):
        """Conta tutti i record"""
        s = f"""SELECT COUNT(*) as total FROM {self.table}"""
        result = self.execute(s, one=True)
        return result[0] if result else 0

    def count_search(self, data):
        """Conta record con criteri specifici"""
        s = f"""SELECT COUNT(*) as total FROM {self.table} WHERE {' AND '.join([f'{key} = ?' for key in data.keys()])}"""
        result = self.execute(s, tuple(data.values()), one=True)
        return result[0] if result else 0

    def statment(self, query,data=None, fetch:bool=False, one:bool=False):
        return self.execute(query=query,data=data, fetch=fetch, one=one)    
        
    def truncate(self):
        """Svuota la tabella"""
        s = f"""DELETE FROM {self.table}"""
        self.execute(s)
        return True

    
    def execute(self, query, data=None, fetch=False, one=False):
        """Esegue una query SQL"""
        try:
            self.exception_table()
        
            if not hasattr(self, '_conn'):
                self._conn = ConnectionSqlite()
        
            row_factory_needed = fetch or one
        
            cursor = self._conn.getCursor(row_factory=row_factory_needed)
        
            result = None
            if data is not None:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            
            if one:
                result = cursor.fetchone()
            elif fetch:
                result = cursor.fetchall()
            else:
                result = cursor.lastrowid  
            cursor.connection.commit()
        
            return result
        except Exception as e:
            raise ExceptionRequest(message=f"""Execute query generate exception: {e}""",status_code=409)
    
    def exception_table(self):
        if self.table is None:
            raise ExceptionRequest(message="Table not found",status_code=400)
        return True