from typing import List
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from .prompts import (
    retrieval_router_prompt, 
    direct_generate_prompt, 
    is_relevant_docs_prompt,
    context_generation_prompt
    )
from ..model.llm_model import llm
from ..embeddings.vector_store import create_embeddings
from ..schema.schema import State, RetrieveDecision, RelevanceDecision


decide_retrieval_prompt = ChatPromptTemplate.from_messages(retrieval_router_prompt)
should_retrieve_llm = llm.with_structured_output(RetrieveDecision)

def decide_retrieval(state: "State"):
    decision: RetrieveDecision = should_retrieve_llm.invoke(
        decide_retrieval_prompt.format_messages(question=state["question"])
    )
    return {"need_retrieval": decision.should_retrieve}


direct_generation_prompt = ChatPromptTemplate.from_messages(direct_generate_prompt)

def generate_direct(state: State):
    output = llm.invoke(
        direct_generation_prompt.format_messages(
            question=state["question"]
        )
    )
    return {"answer": output.content}


def retrieve(state: State):
    vector_store = create_embeddings()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    return {"docs": retriever.invoke(state["question"])}


is_relevant_prompt = ChatPromptTemplate.from_messages(is_relevant_docs_prompt)
relevance_llm = llm.with_structured_output(RelevanceDecision)

def is_relevant(state: State):
    
    relevant_docs: List[Document] = []

    for doc in state["docs"]:
        decision: RelevanceDecision = relevance_llm.invoke(
            is_relevant_prompt.format_messages(
                question=state["question"],
                document=doc.page_content
            )
        )

        if decision.is_relevant:
            relevant_docs.append(doc)

    return {"relevant_docs": relevant_docs}


rag_generation_prompt = ChatPromptTemplate.from_messages(context_generation_prompt)

def generate_from_context(state: State):
    # Stuff relevant docs into one block
    context = "\n\n---\n\n".join(
        [d.page_content for d in state.get("relevant_docs", [])]
    ).strip()

    if not context:
        return {"answer": "No relevant document found.", "context": ""}

    out = llm.invoke(
        rag_generation_prompt.format_messages(
            question=state["question"],
            context=context
        )
    )
    return {"answer": out.content, "context": context}


def no_relevant_docs(state: State):
    return {"answer": "No relevant document found.", "context": ""}