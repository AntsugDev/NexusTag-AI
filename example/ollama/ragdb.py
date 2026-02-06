import os 
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import uuid
from dotenv import load_dotenv
import psycopg
from psycopg import OperationalError
import json

INSERT_DOCUMENT = """
INSERT INTO soa.rag_documents (tag,file_name, chunk_id, chunk_text, embedding, chunk_order, metadata)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""
class RagDb:
    def __init__(self):
       self.conn = None
       load_dotenv()
    
    def connecting (self):
        conn_string = f"host={os.getenv('DB_HOST')} dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASSWORD')} port={os.getenv('DB_PORT')}"
        self.conn = psycopg.connect(conn_string)
        if not self.conn:
            raise Exception("Failed to connect to the database")

    def insert_document(self,tag, file_name, chunk_text, embedding, chunk_order, metadata):
        try:
            self.connecting()
            with self.conn.cursor() as cursor:
                file_id = str(uuid.uuid4())
                cursor.execute(INSERT_DOCUMENT, (tag,file_name, file_id, chunk_text, embedding, chunk_order,  json.dumps(metadata)))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return None

    def select_document(self,tag): 
        try:
            self.connecting()
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM soa.rag_documents WHERE tag = %s", (tag,))
                return cursor.fetchall()
        except Exception as e:
            print(e)
            return None