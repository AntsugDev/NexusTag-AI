from scheduler.scheduler import Scheduler
class DocumentsJobs(Scheduler):
    def __init__(self):
        super().__init__("documents_jobs", trigger="interval", minutes=30)

    def handle(self):
        try:
            from database.model.documents import Documents
            documents = Documents()
            documents_ready = documents.get_documents_ready_to_process()
            for document in documents_ready:
                from file.read import ReadFileCustom
                ReadFileCustom.get_instance(document["name_file"], document["user_id"])
                documents.update_read(document["id"])
        except Exception as e:
            raise e