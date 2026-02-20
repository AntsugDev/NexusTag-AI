from scheduler.scheduler import Scheduler
import datetime
from scheduler.status import scheduler_status

class DocumentsJobs(Scheduler):
    def __init__(self):
        super().__init__("documents_jobs", trigger="interval", minutes=5)

    def handle(self):
            from database.model.documents import Documents
            import csv
            import os
            
            scheduler_status.set_running(True)
            try:
                documents = Documents()
                documents_ready = documents.get_documents_ready_to_process()
                
                log_file = os.path.join(os.getcwd(), 'scheduler_log.csv')
                file_exists = os.path.isfile(log_file)
                
                if documents_ready:
                    print(f"[{datetime.datetime.now()}] Scheduler: Found {len(documents_ready)} documents to process.")
                    
                with open(log_file, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    if not file_exists:
                        writer.writerow(['TIMESTAMP', 'FILE', 'STATO', 'NOTE', 'ECCEZIONE'])
                    
                    for index, document in enumerate(documents_ready):
                        print(f"[{datetime.datetime.now()}] Processing document: {document['name_file']} (ID: {document['id']})")
                        
                        tries = 0
                        max_tries = 3
                        worked = False
                        last_error = ""
                        
                        while tries < max_tries and not worked:
                            tries += 1
                            try:
                                documents.update_pending(document["id"])
                                from file.read import ReadFileCustom
                                file_path = os.path.join(os.getcwd(), 'import-data', document["name_file"])
                                
                                worked = ReadFileCustom.get_instance(file_path, document["id"])
                                
                                if worked:
                                    documents.update_processed(document["id"])
                                    writer.writerow([datetime.datetime.now(), document['name_file'], 'PROCESSED', f'Success at try {tries}', ''])
                                    break
                                else:
                                    last_error = "Processing failed without specific error"
                                    writer.writerow([datetime.datetime.now(), document['name_file'], 'FAILED', f'Attempt {tries} failed', last_error])
                            
                            except Exception as e:
                                last_error = str(e)
                                print(f"[{datetime.datetime.now()}] Attempt {tries} error for {document['name_file']}: {last_error}")
                                writer.writerow([datetime.datetime.now(), document['name_file'], 'ERROR', f'Attempt {tries} exception', last_error])
                        
                        if not worked:
                            documents.update_error(document["id"])
                            self.failed({
                                "document_id": document["id"],
                                "row_id": index,
                                "meta_data": documents.select_document(document["id"]),
                                "exception": f"Failed after {max_tries} attempts. Last error: {last_error}"
                            })
            finally:
                scheduler_status.set_running(False)

          