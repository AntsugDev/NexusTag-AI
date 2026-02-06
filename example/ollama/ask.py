import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import ollama
import numpy as np
from ragdb import RagDb
import json

class Ask:
    def __init__(self):
        self.ragdb = RagDb()
        self.tag = "RAG_pipeline_reale"
        self.docs = self.ragdb.select_document(self.tag)
        self.k = 3
    #Come Estrarre il contenuto semantico?
    def ask(self):
        question = input("Ask a question: ")
        olresponse = ollama.embed(model='llama3', input=question)
        question_embedding = np.array(olresponse.embeddings)
        score_docs = []
        for doc in self.docs:
            doc_embedding = doc[4]
            similarity = self.cosine_similarity(question_embedding, doc_embedding)
            score_docs.append(similarity)
        top_k_idx = np.argsort(score_docs)[-self.k:][::-1] 
        respone = []
        for i in top_k_idx:
            respone.append(self.docs[i][3])
        context =  "\n\n\r".join(respone)
        return self.chat(question, context)
   

    def cosine_similarity(self,a,b):    
        try:
            b = np.array(b).flatten()
            a = a.flatten()
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        except Exception as e:
            raise e

    def chat(self, ask, response):
        try:
            question = f"""Il contesto è: 
            {response};

            {ask}
            
            """
            chat = ollama.chat(model='llama3', 
            messages=[
                 {"role": "system", "content": "Rispondi usando SOLO il contesto fornito."},
                 {"role": "user", "content": question},
            ])
            return chat.message.content
            
        except Exception as e:
            raise e
       


if __name__ == "__main__":
    ask = Ask()
    response = ask.ask()
    print(response)
    