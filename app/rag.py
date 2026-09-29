results = collection.query(
    query_texts=[question],
    n_results=3
)

documents = results.get("documents", [[]])[0]
metadatas = results.get("metadatas", [[]])[0]

if not documents:
    return {
        "answer": "Sorry, I could not find relevant information in the Zepto knowledge base.",
        "sources": [],
        "confidence": 0.0
    }

sources = [
    meta.get("source", "unknown")
    for meta in metadatas
    if meta
]

context = "\n\n".join(documents)

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a Zepto customer support assistant. "
                "Use only the retrieved context to answer."
            )
        },
        {
            "role": "user",
            "content": f"""
            Context:
            {context}

            Question:
            {question}
            """
        }
    ],
    temperature=0.2
)

answer = response.choices[0].message.content

return {
    "answer": answer,
    "sources": sources,
    "confidence": 0.90
}
