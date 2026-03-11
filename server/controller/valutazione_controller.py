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
from form_request.evalutations_request import EvaluationsRequest
from form_request.ask_request import AskRequest,AskTryning
# import nltk
# from nltk.tokenize import sent_tokenize
import re
load_dotenv()

import os
import random
import statistics
import ast
# nltk.download('punkt')

def valutazione_controller(valutazione_router: APIRouter):

    def extract_data_for_evaluation(chunks_raw, evaluations_raw = None):
        try:
            if chunks_raw is None:
                return None
            if not isinstance(chunks_raw, list):
                chunks_raw = [chunks_raw]
            
            chunks = []
            for c in chunks_raw:
                if hasattr(c, 'keys'): 
                    chunks.append({k: c[k] for k in c.keys()})
                else:
                    chunks.append(dict(c))
                
            total_chunks = len(chunks)
            if total_chunks == 0:
                return None

            token_counts = [c.get('token_count', 0) for c in chunks]
            avg_tokens = statistics.mean(token_counts) if token_counts else 0
            stdev_tokens = statistics.stdev(token_counts) if len(token_counts) > 1 else 0

            if evaluations_raw is None: 
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
            selection = []
            
            if evaluations_raw is None:
                random_samples = []
                if middle_chunks:
                    actual_n = min(len(middle_chunks), n_random)
                    random_samples = random.sample(middle_chunks, actual_n)
                selection = [first] + random_samples + [last] if total_chunks > 1 else [first]
            else:
                row = evaluations_raw.get("evalutation_for_row")
                if isinstance(row, str):
                    try:
                        row = ast.literal_eval(row)
                    except:
                        row = []
                
                if row:
                    chunk_map = {c.get('id'): c for c in chunks}
                    for r in row:
                        r_dict = dict(r)
                        cid = r_dict.get("chunk_id")
                        chunk = chunk_map.get(cid)
                        if chunk:
                            item = chunk.copy()
                            item['rating'] = r_dict.get('rating', 0)
                            selection.append(item)
                
                if not selection:
                    # Fallback if row is empty or invalid
                    selection = [first] + [last] if total_chunks > 1 else [first]
            for index,item in enumerate(selection):
                item['order'] = index+1
                current_tokens = item.get('token_count', 0)
                item['global_avg'] = round(avg_tokens, 2)
                item['deviation'] = round(current_tokens - avg_tokens, 2)
                item['range_token'] = current_tokens > int(os.getenv('K_MIN_TOKEN')) and current_tokens < int(os.getenv('K_MAX_TOKEN'))

            # ask = generate_ask(selection)
            # inserisco in una tabella e faccio partire lo scheduler, dove gli passo anche il documento_id, il chunk_id
            


            return {
                "chunks": selection,
                "stats": {
                    "total_chunks": total_chunks,
                    "avg_tokens": round(avg_tokens, 2),
                    "stdev_tokens": round(stdev_tokens, 2),
                    "total_tokens": sum(token_counts),
                    "min_token": int(os.getenv('K_MIN_TOKEN')),
                    "max_token": int(os.getenv('K_MAX_TOKEN')),
                    
                },
                "evaluations": evaluations_raw,
               
            }
        except Exception as e:
            print(f"Errore durante l'estrazione dati valutazione: {e}")
            raise e  

    def generate_ask(chunks):
        try:
            content = ""
            for chunk in chunks:
                content += str(chunk.get("content"))
            sentences = re.split(r'[.!?]\s+', content)
            sample_5 = random.sample(sentences, k=min(2, len(sentences)))
            return sample_5
            
        except Exception as e:
            print(f"Errore durante la generazione ask: {e}")
            raise e

    @valutazione_router.post("/ask",tags=["valutations"], description="Extract asks for testing embeding")
    def extract_ask(data: AskRequest, user: dict = Depends(verify_token)):
        try:
            if user.get("username") != "admin":
                raise HTTPException(status_code=403, detail="Forbidden: Admin only")
            d = dict(data)
            ask = generate_ask(d.get("chunks"))
            from database.model.queries import Queries
            q = Queries()
            response =[]
            for a in ask:
                insert = q.set_query({
                          "user_id": user.get('id'),
                          "query": a,
                          "is_evaluation": 1,
                          "document_id":d.get("document_id")
                })
                if insert:
                    response.append({
                        'id': insert, 'ask': a
                    })    
            return response(msg="Asking", data=response)
            
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)
    
    @valutazione_router.post("/ask/tryning",tags=["valutations"], description="Testing the ask for content")
    def ask_tryning(data: AskTryning, user: dict = Depends(verify_token)):
        try:
           if user.get("username") != "admin":
                raise HTTPException(status_code=403, detail="Forbidden: Admin only")
           from database.model.embed_model import EmbedModel
           e = EmbedModel()
           r = e.similarity(query_id=data.id_query)     
           return response(msg="Similarity", data=r)
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)    

    @valutazione_router.get("/{document_id}",tags=["valutations"], description="Get valutation for document")
    def valutazione(document_id: int,user: dict = Depends(verify_token)):
        try:
            if user.get("username") != "admin":
                raise HTTPException(status_code=403, detail="Forbidden: Admin only")
            from database.model.evalutations import Evaluations
            e = Evaluations()
            evalutations = e.get_evaluation(document_id=document_id)
            evalutations = dict(evalutations[0]) if evalutations else None
            from database.model.chunks_table import ChunkTable
            chunk_table = ChunkTable()
            data = chunk_table.get_chunks_by_document_id(document_id, join_table=[
                    {
                        "typed": "LEFT",
                        "table": "t_strategy_chunk",
                        "on": "chunks.strategy_chunk = t_strategy_chunk.id"
                    }
                ], columns=["chunks.*", "t_strategy_chunk.name"])
            r = extract_data_for_evaluation(data,evalutations)
            return response(msg="Valutations", data=r)
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)

    @valutazione_router.post("/",tags=["valutations"], description="Insert valutation")
    def insert_valutation(evaluations_request: EvaluationsRequest,user: dict = Depends(verify_token)):
        try:
            if user.get("username") != "admin":
                raise HTTPException(status_code=403, detail="Forbidden: Admin only")
            from database.model.evalutations import Evaluations
            evaluations = Evaluations()
            evaluations.insert_evaluation(evaluations_request)
            return response(msg="Valutation inserted", data={}, status_code=201)
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)

    @valutazione_router.get("/",tags=["valutations"], description="Get valutations")
    def get_valutations(page: int = 1, limit: int = 5,user: dict = Depends(verify_token)):
        try:
            if user.get("username") != "admin":
                raise HTTPException(status_code=403, detail="Forbidden: Admin only")
            from database.model.evalutations import Evaluations
            evaluations = Evaluations()
            data = evaluations.get_all_evaluations(page=page, limit=limit, join_table=[
                    {
                        "typed": "LEFT",
                        "table": "t_strategy_chunk",
                        "on": "evaluations.strategy_chunk = t_strategy_chunk.id"
                    },
                     {
                        "typed": "LEFT",
                        "table": "t_topic",
                        "on": "evaluations.topic = t_topic.id"
                    },
                     {
                        "typed": "LEFT",
                        "table": "documents",
                        "on": "evaluations.document_id = documents.id"
                    }
                ], columns=["evaluations.*", "t_strategy_chunk.name as strategy_name", "t_topic.name as topic_name", "documents.name_file","documents.mime_type"])
            total = evaluations.count_search(data=None)
            return response(msg="Valutations", data={
                "items": [dict(item) for item in data],
                "total": total,
                "page": page,
                "limit": limit
            })
        except Exception as e:
            raise ExceptionRequest(message=str(e), status_code=422)        