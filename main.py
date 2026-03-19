import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.conn_sqlite import ConnectionSqlite

if __name__ == "__main__":
    try:
        conn = ConnectionSqlite()
        conn.migration(is_force=1)
        conn.close()
    except Exception as e:
        raise e