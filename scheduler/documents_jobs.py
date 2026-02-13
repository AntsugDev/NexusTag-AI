from scheduler.scheduler import Scheduler
import datetime
class DocumentsJobs(Scheduler):
    def __init__(self):
        super().__init__("documents_jobs", trigger="interval", minutes=5)

    def handle(self):
        
            from database.model.documents import Documents
            documents = Documents()
            documents_ready = documents.get_documents_ready_to_process()
            if documents_ready:
                print(f"[{datetime.datetime.now()}] Scheduler: Found {len(documents_ready)} documents to process.")
                
            for index, document in enumerate(documents_ready):
                print(f"[{datetime.datetime.now()}] Processing document: {document['name_file']} (ID: {document['id']})")
                try:
                    documents.update_pending(document["id"])
                    from file.read import ReadFileCustom
                    import os
                    file_path = os.path.join(os.getcwd(), 'import-data', document["name_file"])
                    worked = ReadFileCustom.get_instance(file_path, document["id"])
                    if worked:
                        documents.update_processed(document["id"])
                    else:
                        self.failed({
                        "document_id": document["id"],
                        "row_id": index,
                        "meta_data": documents.select_document(document["id"]),
                        "exception": worked
                    })   
                    documents.update_error(document["id"])
                except Exception as e:
                    documents.update_error(document["id"])
                    self.failed({
                        "document_id": document["id"],
                        "row_id": index,
                        "meta_data": documents.select_document(document["id"]),
                        "exception": str(e)
                    })  
          