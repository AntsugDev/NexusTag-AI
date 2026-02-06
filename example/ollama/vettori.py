import ollama

text = "Questo è un documento di prova"
emb = ollama.embed(model="llama3", input=text)

print("-"*30+"VETTORI"+"-"*30+"\n")
print(emb)
print("*"*60+"\n")