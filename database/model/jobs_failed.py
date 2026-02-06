class JobsFailed(ModelGeneral):
    def __init__(self):
        self.table = "jobs_failed"

    def insert_job_failed(self,data):
        return self.insert({
            "document_id": data.document_id,
            "row_id": data.row_id,
            "meta_data": data.meta_data,
            "exception": data.exception
        })