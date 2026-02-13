from scheduler.scheduler import Scheduler
class DocumentsJobs(Scheduler):
    def __init__(self):
        super().__init__("documents_jobs", trigger="cron", hour=3, minute=0)

    def handle(self):
        
            from database.model.documents import Documents
            documents = Documents()
            documents_ready = documents.get_documents_ready_to_process()
            for index, document in enumerate(documents_ready):
                try:
                    from file.read import ReadFileCustom
                    worked = ReadFileCustom.get_instance(document["name_file"], document["user_id"])
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
          