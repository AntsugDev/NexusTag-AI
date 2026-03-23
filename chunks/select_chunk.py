class SelectChunk:
    def __init__(self,mime_type:str, document_id:int):
        match mime_type:

            case "text/plain":
                
            case _:    
                raise ValueError(f"Unsupported mime type: {mime_type}")
            # case "application/pdf":
            # case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                
            # case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
               
            # case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
                
            #     raise ValueError(f"Unsupported mime type: {mime_type}")
    
    