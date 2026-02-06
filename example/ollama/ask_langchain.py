import os
import sys
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_ollama  import OllamaEmbeddings, ChatOllama
from langchain_community.llms import Ollama
import mimetypes
import numpy as np
from ragdb import RagDb
import time
import json

ragdb = RagDb()
embeddings = OllamaEmbeddings(model="llama3")
k = 3
chat = ChatOllama(model="llama3", name="test ollama langchain",disable_streaming=False)
assistent = []

def cosine_similarity(a,b):    
        try:
            b = np.array(b).flatten()
            a = np.array(a).flatten()
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        except Exception as e:
            raise e

def ask():
    try:
        question = input("Ask a question: ")
        question_embedding = embeddings.embed_query(question)
        all_documents = ragdb.select_document('RAG_pipeline_reale_langchain')
        score = []
        for document in all_documents:
            similarity = cosine_similarity(question_embedding, document['embedding'])
            score.append(similarity)
        top_k_idx = np.argsort(score)[-k:][::-1]
        respone = []
        for i in top_k_idx:
            respone.append(all_documents[i]['content'])
        context = "\n\n\r".join(respone)+ ", "+question
        return context
        
    except Exception as e:
        print(f"Error asking question: {e}")
        sys.exit(1)

def chatLLm():
    try:
        context = ask()
        messages= [
            {"role": "system", "content": "Sei un assistente che risponde in italiano e spiega le RAG per l'AI"},
            {"role": "user", "content": context}
        ]
        response = chat.invoke(messages)
        assistent.append(response.content)
        print(f"Assistant response: {response.content}")
    except Exception as e:
        print(f"Error asking question: {e}")
        sys.exit(1)

text = None
file_path = os.path.join(os.path.dirname(__file__), 'RAG_pipeline_reale.md')
mimetype, encoding = mimetypes.guess_type(file_path)
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

if text is not None:
    try:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=20,
            length_function=len,
            separators=["#","##", "###"],
            is_separator_regex=False
        )
        chunks = splitter.split_text(text)
        if len(chunks) > 0:
            for i, chunk in enumerate(chunks):
                embedding = embeddings.embed_query(chunk)
                metadata = {
                    'tag': 'RAG_pipeline_reale_langchain',
                    'file_name': 'RAG_pipeline_reale.md',
                    'size': os.path.getsize(file_path),
                    'mine_type':mimetype,
                    'encoding':encoding
                }
                ragdb.insert_document(metadata['tag'], metadata['file_name'], chunk,json.dumps(embedding), (i+1), metadata)
            time.sleep(1)
        chatLLm();
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)      