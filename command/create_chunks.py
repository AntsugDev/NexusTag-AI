print("From this command you can create chunks of documents ...")
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.model.documents import Documents

try:
    documents = Documents()
    response  = documents.get_documents_ready_to_process()
    for index,document in enumerate(response):
        row = dict(document)
        tries = 0
        max_tries = 3
        worked = False
        last_error = ""
                        
        while tries < max_tries and not worked:
            tries += 1
            print(f"Try {tries} for document: {document['name_file']} ")
            try:
                documents.update_pending(document['id'])
                from file.read import ReadFileCustom
                file_path = os.path.join(os.getcwd(), 'import-data', document['name_file'])
                
                worked = ReadFileCustom.get_instance(file_path, document['id'])
                
                if worked:
                    documents.update_processed(document['id'])
                    break
                else:
                    raise Exception("Processing failed without specific error")
            except Exception as e:
                if tries == max_tries:
                    documents.update_error(row.get("id"))
                    tries += 1
                    raise e
        
except Exception as e:
    print(e)    