from langchain_core.prompts import ChatPromptTemplate

decide_retrieval_prompt = ChatPromptTemplate.from_messages([
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
])


direct_generation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "Answer the question using only your general knowledge.\n"
        "Do NOT assume access to external documents.\n"
        "If you are unsure or the answer requires specific sources, say:\n"
        "'I don't know based on my general knowledge.'"
    ),
    ("human", "{question}"),
])


is_relevant_prompt = ChatPromptTemplate.from_messages([
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
])


rag_generation_prompt = ChatPromptTemplate.from_messages([
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
])


issup_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are verifying whether the ANSWER is supported by the CONTEXT.\n"
            "Return JSON with keys: issup, evidence.\n"
            "issup must be one of: fully_supported, partially_supported, no_support.\n\n"
            "How to decide issup:\n"
            "- fully_supported:\n"
            "  Every meaningful claim is explicitly supported by CONTEXT, and the ANSWER does NOT introduce\n"
            "  any qualitative/interpretive words that are not present in CONTEXT.\n"
            "  (Examples of disallowed words unless present in CONTEXT: culture, generous, robust, designed to,\n"
            "  supports professional development, best-in-class, employee-first, etc.)\n\n"
            "- partially_supported:\n"
            "  The core facts are supported, BUT the ANSWER includes ANY abstraction, interpretation, or qualitative\n"
            "  phrasing not explicitly stated in CONTEXT (e.g., calling policies 'culture', saying leave is 'generous',\n"
            "  or inferring outcomes like 'supports professional development').\n\n"
            "- no_support:\n"
            "  The key claims are not supported by CONTEXT.\n\n"
            "Rules:\n"
            "- Be strict: if you see ANY unsupported qualitative/interpretive phrasing, choose partially_supported.\n"
            "- If the answer is mostly unrelated to the question or unsupported, choose no_support.\n"
            "- Evidence: include up to 3 short direct quotes from CONTEXT that support the supported parts.\n"
            "- Do not use outside knowledge."
        ),
        (
            "human",
            "Question:\n{question}\n\n"
            "Answer:\n{answer}\n\n"
            "Context:\n{context}\n"
        ),
    ]
)