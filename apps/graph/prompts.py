retrieval_router_prompt = [
    (
        "system",
        "You decide whether retrieval is needed.\n"
        "Return JSON that matches this schema:\n"
        "{{'should_retrieve': boolean}}\n\n"
        "Guidelines:\n"
        "- should_retrieve=True if answering requires specific facts, citations, or info likely not in the model.\n"
        "- should_retrieve=False for general explanations, definitions, or reasoning that doesn't need sources.\n"
        "- If unsure, choose True."
    ),
    ("human", "Question: {question}"),
]

direct_generate_prompt = [
    (
        "system",
        "Answer the question using only your general knowledge.\n"
        "Do NOT assume access to external documents.\n"
        "If you are unsure or the answer requires specific sources, say:\n"
        "'I don't know based on my general knowledge.'"
    ),
    ("human", "{question}"),
]

is_relevant_docs_prompt = [
    (
        "system",
        "You are judging document relevance.\n"
        "Return JSON that matches this schema:\n"
        "{{'is_relevant': boolean}}\n\n"
        "A document is relevant if it contains information useful for answering the question."
    ),
    (
        "human",
        "Question:\n{question}\n\nDocument:\n{document}"
    ),
]

context_generation_prompt = [
    (
        "system",
        "You are a business RAG assistant.\n"
        "Answer the user's question using ONLY the provided context.\n"
        "If the context does not contain enough information, say:\n"
        "'No relevant document found.'\n"
        "Do not use outside knowledge.\n"
    ),
    (
        "human",
        "Question:\n{question}\n\n"
        "Context:\n{context}\n"
    ),
]