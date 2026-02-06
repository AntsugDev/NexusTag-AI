from general_chunck import GeneralChunck
from langchain_text_splitters import  RecursiveCharacterTextSplitter
# file log, txt, markdown e sql
class SimpleChunk(GeneralChunck):
    def __init__ (self, file, type_file, document_id):
        super().__init__(file, type_file, document_id)
        self.get_content = None
        with open(self.file, 'r',  encoding='utf-8') as f:
            self.get_content = f.read()
        
        self.separator_standard = ["\n", "\r\n"]

        if self.type_file == 'md':
            self.separator_standard = ["#", "##", "###", "\n\n", "\n", " "]
        elif self.type_file == 'sql':
            self.get_content = self.get_content.upper()
            self.separator_standard = ["SELECT", "UPDATE", "INSERT", "DELETE", "\n\n", "\r\n", "\n"]
            self.setToken(300)

    def chunck(self) -> list[dict]:
        try:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.standard_token,
                chunk_overlap=self.standard_overlap, # Usiamo la variabile calcolata
                length_function=len,
                separators=self.separator_standard,
                is_separator_regex=False
            )
            splits = splitter.split_text(self.get_content)
            
            # Trasformiamo in lista di dict con metadati
            result = []
            for i, text in enumerate(splits):
                result.append({
                    "content": text,
                    "metadata": {
                        "chunk_order": i,
                        "type": self.type_file,
                        "char_count": len(text)
                    }
                })
            return result
        except Exception as e:
            raise e