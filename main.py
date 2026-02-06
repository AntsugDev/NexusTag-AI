from database.conn_sqlite import ConnectionSqlite
import uvicorn
import os
from server.server import app
ENV = os.getenv("ENV", "development")
if __name__ == "__main__":
   c = ConnectionSqlite()
   c.migration()
   if ENV == "development":   
      uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info")

    