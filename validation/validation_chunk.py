import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.model.documents import Documents
from database.model.jobs_failed import JobsFailed
from file.read import ReadFileCustom

doc = Documents()
documents = doc.get_documents_ready_to_process()

def path_complete(file_name):
    return os.path.join(os.path.dirname(__file__).replace('validation', 'import-data'), file_name)

def convert_in_dict(data):
    if data:
        return dict(data)
    return data

def failed(data):
    
    jobs_failed = JobsFailed()
    jobs_failed.insert_job_failed(data)

print("\u26A0 Validazione Documenti ... \n ")
print("-"*60+"\n")
for index,document in enumerate(documents):
    try:
        print(f"\u2605 Row {index+1}/{len(documents)} \n")
        datatmp = convert_in_dict(document)
        path = path_complete(datatmp['name_file'])
        if os.path.exists(path):
            worked = ReadFileCustom().get_instance(path, datatmp['id'])
            if worked:
                doc.update_processed(datatmp['id'])
                print(f"\u2713 Success chunck \n"+"*"*60+"\n")
                print(worked)
            else:
                doc.update_error(datatmp['id'])
                # failed({
                #     'id ': datatmp['id'],
                #     'row_id': index,
                #     'meta_data': doc.select_document(datatmp['id']),
                #     'exception': 'Errore durante la validazione del documento'
                # })

        else: 
            raise Exception(f"File {path} non esiste") 
    except Exception as e:
        print(f"eccezione di ... {str(e)}")
        # failed({
        #             'id': datatmp['id'],
        #             'row_id': index,
        #             'meta_data': doc.select_document(datatmp['id']),
        #             'exception': str(e)
        #         })

