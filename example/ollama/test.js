const document = [
    "Ollama è un server locale che permette di eseguire Large Language Model.",
    "La RAG è un sistema che combina retrieval + LLM per rispondere usando documenti.",
    "Gli embedding trasformano testo in vettori numerici per confronti di similarità."
];
 try{  
    const response = fetch('http://localhost:11434/api/embed', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        model: 'llama3',
        input: document
    })
})
response.then(res => {
    console.log(res)
})
}catch(error){
    console.log(error)
}
