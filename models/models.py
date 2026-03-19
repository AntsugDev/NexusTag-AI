import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.conn_sqlite import ConnectionSqlite
from datetime import datetime

class Models:
    def __init__(self):
        self.table= None
        self.default_order_by = None
        self.default_sort = "ASC"
        self.columns = []
        self.join = []
        self.conn = ConnectionSqlite()
        """
          row_factory_needed = fetch or one
          cursor = self._conn.getCursor(row_factory=row_factory_needed)
        """

    def __join(self):
        """
            Join sarà una dict che deve contenere le seguenti chiavi:
            - table: nome della tabella da joinare
            - on: condizione di join
            - type: tipo di join (INNER, LEFT, RIGHT, FULL)
        """
        join_str = ""
        if self.join:
            for join in self.join:
                join_str += f"INNER JOIN {join['table']} ON ({join['table']}.id = {self.table}.{join['table_id']} AND {join['table']}.deleted_at IS NULL)"
        return join_str

    def __where(self, where):
        """
            Where sarà una dict che deve contenere le seguenti chiavi:
            - column: nome della colonna da filtrare
            - operator: operatore da usare (=,like,in,not in, ecc.)
            - value: valore da cercare
            - type: tipo di where (AND, OR)
        """
        where_str = ""
        if where:
            for where in where:
                where_str += f"{where['type']} {where['column']} {where['operator']} {where['value']}"

            if where_str == "":
                where_str = f" DELETED_AT IS NULL"    
            else:
                where_str = f" {where_str} AND DELETED_AT IS NULL"    
        return where_str    

    def __columns(self):
        """
            è un array di stringhe che rappresenta le colonne da selezionare
        """
        columns_str = "*"
        if self.columns:
            for column in self.columns:
                columns_str += f"{column},"
            columns_str += "created_at,updated_at"    
        return columns_str

    def paginate(self,where:[dict]=None, page=1, per_page=10, order_by=self.default_order_by, sort=self.default_sort):
        try:
            cursor = self.conn.getCursor(True)
            join_str = self.__join()
            where_str = self.__where(where)
            columns_str = self.__columns()
            cursor.execute(f'SELECT {columns_str} FROM {self.table} {join_str} {where_str} ORDER BY {order_by} {sort} LIMIT {per_page} OFFSET {(page-1)*per_page}')
            return cursor.fetchall()
        except Exception as e:
            raise e        
    
    
    def list(self, where:[dict]=None):
        try:
            cursor = self.conn.getCursor(True)
            join_str = self.__join()
            where_str = self.__where(where)
            columns_str = self.__columns()
            cursor.execute(f'SELECT {columns_str} FROM {self.table} {join_str} {where_str}')
            return cursor.fetchall()
        except Exception as e:
            raise e

    def find(self,id:int):        
        try:
            cursor = self.conn.getCursor(True)
            join_str = self.__join()
            columns_str = self.__columns()
            cursor.execute(f'SELECT {columns_str} FROM {self.table} {join_str} WHERE id = {id}')
            return cursor.fetchone()
        except Exception as e:
            raise e

    def findBy(self,where:[dict]=None):        
        try:
            cursor = self.conn.getCursor(True)
            join_str = self.__join()
            where_str = self.__where(where)
            columns_str = self.__columns()
            cursor.execute(f'SELECT {columns_str} FROM {self.table} {join_str} {where_str}')
            return cursor.fetchone()
        except Exception as e:
            raise e
    def insert(self, data:dict):
        try:
            keys = ",".join(data.keys())
            keys += ",created_at"
            values = ",".join([f"'{value}'" for value in data.values()])
            values += f",'{datetime.now()}'"
            cursor = self.conn.getCursor()
            cursor.execute(f'INSERT INTO {self.table} ({keys}) VALUES ({values})')
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            raise e

    def updateById(self, id:int, data:[dict]):
        try:
            """
            data = [
                {'column': 'name', 'value': 'John Doe', 'operator': '=', 'type': 'AND'},
                {'column': 'email', 'value': 'john.doe@example.com', 'operator': '=', 'type': 'OR'}
            ]
            """
            set_str = ",".join([f"{item['column']} = '{item['value']}'" for item in data])
            set_str += ",updated_at = '{datetime.now()}'"

            cursor = self.conn.getCursor()
            cursor.execute(f'UPDATE {self.table} SET {set_str} WHERE id = {id}')
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            raise e

    def updateByCondition(self, where:[dict], data:[dict]):
        try:
            """
            data = [
                {'column': 'name', 'value': 'John Doe', 'operator': '=', 'type': 'AND'},
                {'column': 'email', 'value': 'john.doe@example.com', 'operator': '=', 'type': 'OR'}
            ]
            """
            where_str = self.__where(where)
            set_str = ",".join([f"{item['column']} = '{item['value']}'" for item in data])
            set_str += ",updated_at = '{datetime.now()}'"

            cursor = self.conn.getCursor()
            cursor.execute(f'UPDATE {self.table} SET {set_str} {where_str}')
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            raise e 

    def deleteById(self, id:int):
        try:
            cursor = self.conn.getCursor()
            cursor.execute(f'UPDATE {self.table} SET deleted_at = {datetime.now()} WHERE id = {id}')
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            raise e

    def deleteByCondition(self, where:[dict]):
        try:
            where_str = self.__where(where)
            cursor = self.conn.getCursor()
            cursor.execute(f'UPDATE {self.table} SET deleted_at = {datetime.now()} {where_str}')
            self.conn.commit()
            return cursor.rowcount
        except Exception as e:
            raise e 

    def statment(self, query:str):
        try:
            cursor = self.conn.getCursor(True)
            cursor.execute(query)
            self.conn.commit()
            return cursor.fetchall()
        except Exception as e:
            raise e                              




