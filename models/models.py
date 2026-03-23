import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.conn_sqlite import ConnectionSqlite
from datetime import datetime
import math

class Models:
    def __init__(self):
        self.table= None
        self.default_order_by = 'created_at'
        self.default_sort = "DESC"
        self.columns = []
        self.join = []
        self.conn = ConnectionSqlite()
        """
          row_factory_needed = fetch or one
          cursor = self._conn.getCursor(row_factory=row_factory_needed)
        """

    def all(self, fetch):
        try:
            if fetch is None:
                return None
            return [dict(item) for item in fetch]
        except Exception as e:
            raise e      

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
            - typeof: tipo di valore (string, number)
        """
        where_str = ""
        if where:
            for k,w in enumerate(where):
                v = f"'{w['value']}'" if isinstance(w['value'],str) else w['value']
                where_str += f"{ 'WHERE' if k == 0 else w['type']} {w['column']} {w['operator']} {v}"

            if where_str == "":
                where_str = f" WHERE ({self.table}.deleted_at = '' OR {self.table}.deleted_at IS NULL)"    
            else:
                where_str = f" {where_str} AND ({self.table}.deleted_at = '' OR {self.table}.deleted_at IS NULL)"    
        else:         
            where_str = f" WHERE ({self.table}.deleted_at = '' OR {self.table}.deleted_at IS NULL)"   
        return where_str    

    def __columns(self):
        """
            è un array di stringhe che rappresenta le colonne da selezionare
        """
        columns_str = ""
        if self.columns:
            for column in self.columns:
                c = column if column != 'id' else f"{self.table}.id"
                columns_str += f"{c},"
            columns_str += f"strftime('%Y-%m-%d %H:%M:%S',{self.table}.created_at) as created_at,strftime('%Y-%m-%d %H:%M:%S',{self.table}.updated_at) as updated_at"
        else:
            columns_str = f"{self.table}.*"  
        

        return columns_str

    def paginate(self,where:[dict]=None, page=1, per_page=10, orderBy:str=None, sort:str=None):
        try:
            order_by = orderBy if orderBy else self.default_order_by
            sort = sort if sort else self.default_sort
            cursor = self.conn.getCursor(True)
            join_str = self.__join()
            where_str = self.__where(where)
            columns_str = self.__columns()
            cursor.execute(f'SELECT {columns_str} FROM {self.table} {join_str} {where_str} ORDER BY {order_by} {sort} LIMIT {per_page} OFFSET {(page-1)*per_page}')
            response = self.all(cursor.fetchall())
            total_page = math.ceil(len(response)/per_page)
            return {"data":response, "page":page, "per_page":per_page, "total_element":len(response), "total_page":total_page, "order_by":order_by, "sort":sort}
        except Exception as e:
            raise e        
    
    
    def list(self, where:[dict]=None):
        try:
            cursor = self.conn.getCursor(True)
            join_str = self.__join()
            where_str = self.__where(where)
            columns_str = self.__columns()
            cursor.execute(f'SELECT {columns_str} FROM {self.table} {join_str} {where_str}')
            return self.all(cursor.fetchall())
        except Exception as e:
            raise e

    def find(self,id:int):        
        try:
            cursor = self.conn.getCursor(True)
            join_str = self.__join()
            columns_str = self.__columns()
            cursor.execute(f'SELECT {columns_str} FROM {self.table} {join_str} WHERE {self.table}.id = {id}')
            return self.all(cursor.fetchall())
        except Exception as e:
            raise e

    def findBy(self,where:[dict]=None):        
        try:
            cursor = self.conn.getCursor(True)
            join_str = self.__join()
            where_str = self.__where(where)
            columns_str = self.__columns()
            cursor.execute(f'SELECT {columns_str} FROM {self.table} {join_str} {where_str}')
            return self.all(cursor.fetchall())
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
            cursor.connection.commit()
            return cursor.lastrowid
        except Exception as e:
            raise e

    def updateById(self, id:int, data:dict):
        try:
            """
            data = [
                {'column': 'name', 'value': 'John Doe', 'operator': '=', 'type': 'AND'},
                {'column': 'email', 'value': 'john.doe@example.com', 'operator': '=', 'type': 'OR'}
            ]
            """
            set_str = ",".join([f"{key} = '{item}'" for (key,item) in data.items()])
            set_str += f",updated_at = '{datetime.now()}'"


            cursor = self.conn.getCursor()
            cursor.execute(f'UPDATE {self.table} SET {set_str} WHERE id = {id}')
            cursor.connection.commit()
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
            cursor.connection.commit()
            return cursor.rowcount
        except Exception as e:
            raise e 

    def deleteById(self, id:int):
        try:
            cursor = self.conn.getCursor()
            cursor.execute(f"UPDATE {self.table} SET deleted_at = '{datetime.now()}' WHERE id = {id}")
            cursor.connection.commit()
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

    def deleteAll(self):
        try:
            cursor = self.conn.getCursor()
            cursor.execute(f"UPDATE {self.table} SET deleted_at = '{datetime.now()}'")
            cursor.connection.commit()
            return True
        except Exception as e:
            raise e        

    def statment(self, query:str):
        try:
            cursor = self.conn.getCursor(True)
            cursor.execute(query)
            self.conn.commit()
            return self.all(cursor.fetchall())  
        except Exception as e:
            raise e                              




