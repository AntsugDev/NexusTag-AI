import ollama

documento = """
Ollama è un server locale che permette di eseguire Large Language Model
come LLaMA o Mistral senza connessione internet.
Viene usato spesso per RAG e prototipi offline.
"""
prompt = f"""
Usa SOLO le informazioni seguenti per rispondere:

{documento}

Domanda:
A cosa serve Ollama?
"""

response = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': prompt}]
)
print("-"*30+"PRIMO RAG"+"-"*30+"\n")
print(response['message']['content'])

"""
Questo È già RAG, concettualmente:

Retrieval → manuale

Augmentation → testo nel prompt

Generation → LLM

Con quella variabile non stai “addestrando” il modello, ma lo stai istruendo temporaneamente su come rispondere a questa domanda (o a questa conversazione) usando solo quel contenuto.

È una conoscenza effimera, valida solo per quel prompt.

Perché questo è il cuore della RAG

La RAG fa esattamente questo, ma in modo sistematico:

Retrieve → scelgo i documenti rilevanti

Augment → li incollo nel prompt

Generate → il modello risponde

La RAG non rende intelligente il modello.
Rende intelligente l’accesso alle informazioni.

"""