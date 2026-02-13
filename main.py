from database.conn_sqlite import ConnectionSqlite
import uvicorn
import os
from server.server import app
from scheduler.register_scheduler import register_all_jobs
from apscheduler.schedulers.background import BackgroundScheduler

ENV = os.getenv("ENV", "development")

if __name__ == "__main__":
    # c = ConnectionSqlite()
    # c.migration(is_force=1)
    # c.create_base_user()

    # Avvio dello scheduler in background
    scheduler = BackgroundScheduler()
    register_all_jobs(scheduler)
    scheduler.start()

    if ENV == "development":   
        uvicorn.run(app, host="0.0.0.0", port=8081, log_level="info")

    