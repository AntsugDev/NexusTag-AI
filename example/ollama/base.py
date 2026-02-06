import ollama

"""
classico prompt non legato a file
"""
response = ollama.chat(
    model='llama3',
    messages=[
        {'role': 'user', 'content': 'Spiegami cos’è Ollama in una frase'}
    ]
)
print("-"*30+"PROMPT"+"-"*30+"\n")
print(response['message']['content'])

print("-"*60+"\n")
print("-"*30+"CONTESTO"+"-"*30+"\n")

messages = [
    {'role': 'system', 'content': 'Sei un assistente tecnico Python'},
    {'role': 'user', 'content': 'Cos’è Ollama?'},
    {'role': 'assistant', 'content': 'Ollama è un runtime locale per LLM.'},
    {'role': 'user', 'content': 'E a cosa serve in una RAG?'}
]

response = ollama.chat(
    model='llama3',
    messages=messages
)
"""
Il contesto lo gestisci tu, non Ollama.
"""
print(response['message']['content'])