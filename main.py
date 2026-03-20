import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.conn_sqlite import ConnectionSqlite
from server.server import app
import uvicorn

if __name__ == "__main__":
    try:
        conn = ConnectionSqlite()
        conn.migration(is_force=0)
        conn.close()

        if os.getenv("ENVOREMENT") == "local":   
             uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info")
    except Exception as e:
        raise e