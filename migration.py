from database.conn_sqlite import ConnectionSqlite
import shutil
import os

print("Inizio migrazione ...")

c = ConnectionSqlite()
c.migration(is_force=1)
c.create_base_user()

from database.model.strategy import StrategyChunk
s = StrategyChunk()
s.basic_data()
    
shutil.rmtree(os.path.join(os.path.dirname(__file__), 'import-data'))   # cancella tutto
os.makedirs(os.path.join(os.path.dirname(__file__), 'import-data')) 

print("Fine migrazione ...")