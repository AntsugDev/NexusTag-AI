from database.conn_sqlite import ConnectionSqlite

if __name__ == "__main__":
   c = ConnectionSqlite()
   c.migration()
    