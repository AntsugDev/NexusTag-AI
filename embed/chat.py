import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from langchain_ollama  import ChatOllama

class Chat:
    def __init__(self):
        pass

    @staticmethod
    def tryning_chat(self,history:[] = None):
        try:
            chat = ChatOllama(model="llama3", name="Ask rag NexusTag AI",disable_streaming=False)
           

        except Exception as e:
            raise e    