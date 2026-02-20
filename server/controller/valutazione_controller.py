import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from fastapi import APIRouter, HTTPException, Request, File, Form, UploadFile, BackgroundTasks, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from form_request.user_request import UserRequest,PasswordUpdate
from database.model.users import User
from utility.utility import convert_from_pydantic, ExceptionRequest, response
from server.auth import verify_token
import shutil
from dotenv import load_dotenv
load_dotenv()

import os
import random
import statistics

def extract_data_for_evaluation(chunks_raw):
    try:
        if chunks_raw is None:
            return None
            
        # Debugging type
        print(f"DEBUG: chunks_raw type: {type(chunks_raw)}")
        
        # Ensure it's a list
        if not isinstance(chunks_raw, list):
            chunks_raw = [chunks_raw]
            
        chunks = []
        for c in chunks_raw:
            if hasattr(c, 'keys'): # sqlite3.Row has keys()
                chunks.append({k: c[k] for k in c.keys()})
            else:
                chunks.append(dict(c))
                
        total_chunks = len(chunks)
        if total_chunks == 0:
            return None

        token_counts = [c.get('token_count', 0) for c in chunks]
        avg_tokens = statistics.mean(token_counts) if token_counts else 0
        stdev_tokens = statistics.stdev(token_counts) if len(token_counts) > 1 else 0

        try:
            max_random = int(os.getenv('K_MAX_RANDOM_CHUNK', 20))
            min_random = int(os.getenv('K_MIN_RANDOM_CHUNK', 10))
        except (TypeError, ValueError):
            max_random, min_random = 20, 10

        if total_chunks <= min_random:
            n_random = total_chunks
        else:
            n_random = min(max_random, min_random + (total_chunks // 10))
    
        first = chunks[0]
        last = chunks[-1]
        
        middle_chunks = chunks[1:-1]
        random_samples = []
        if middle_chunks:
            actual_n = min(len(middle_chunks), n_random)
            random_samples = random.sample(middle_chunks, actual_n)

        selection = [first] + random_samples + [last]
        for index,item in enumerate(selection):
            item['order'] = index+1
            current_tokens = item.get('token_count', 0)
            item['global_avg'] = round(avg_tokens, 2)
            item['deviation'] = round(current_tokens - avg_tokens, 2)

        return {
            "chunks": selection,
            "stats": {
                "total_chunks": total_chunks,
                "avg_tokens": round(avg_tokens, 2),
                "stdev_tokens": round(stdev_tokens, 2),
                "total_tokens": sum(token_counts)
            }
        }
    except Exception as e:
        print(f"Errore durante l'estrazione dati valutazione: {e}")
        raise e  

def valutazione_controller(router: APIRouter):
    @router.get("/{document_id}",tags=["valutations"], description="Get valutation for document")
    def valutazione(document_id: int,user: dict = Depends(verify_token)):
        try:
            if user.get("username") != "admin":
                raise HTTPException(status_code=403, detail="Forbidden: Admin only")
            from database.model.chunks_table import ChunkTable
            chunk_table = ChunkTable()
            data = chunk_table.get_chunks_by_document_id(document_id)
            r = extract_data_for_evaluation(data)
            return response(msg="Valutations", data=r)
        except Exception as e:
           raise ExceptionRequest(message=str(e), status_code=422)