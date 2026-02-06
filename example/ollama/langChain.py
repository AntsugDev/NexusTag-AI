import os
import sys
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_ollama  import OllamaEmbeddings, ChatOllama
from langchain_community.llms import Ollama
import json
from ragdb import RagDb

headers_to_split_on = [
    ("#", "Titolo 1"),
    ("##", "Titolo 2"), 
    ("1.", "Punto 1"),
    ("2.", "Punto 2"),
]

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=20,
    length_function=len,
    separators=["#","##", "###"],
    is_separator_regex=False
)

# embeddings = OllamaEmbeddings(model="llama3")
# llm = ChatOllama(model="llama3")
# file_path = os.path.join(os.path.dirname(__file__), 'RAG_pipeline_reale.md')
# with open(file_path, 'r', encoding='utf-8') as f:
#     text = f.read()
# chunks = splitter.split_text(text)
# if len(chunks) > 0:
#     for i, chunk in enumerate(chunks):
#       embedding = embeddings.embed_query(chunk)
#       """
#       Insert dentro la tabella embeddings
#       """
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"},
]     
chat = ChatOllama(model="llama3", name="test ollama langchain",disable_streaming=False)
response = chat.invoke(messages)
print(f"Response Assistant: {response.content}")

