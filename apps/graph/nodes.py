from typing import List
from langchain_core.documents import Document
from .prompts import *
from ..model.llm_model import llm
from ..embeddings.vector_store import create_embeddings
from ..schema.schema import *


# ----------------------------
# 1. Decide Retrieval
# ----------------------------
should_retrieve_llm = llm.with_structured_output(RetrieveDecision)

def decide_retrieval(state: "State"):
    decision: RetrieveDecision = should_retrieve_llm.invoke(
        decide_retrieval_prompt.format_messages(question=str(state["question"]))
    )
    return {"need_retrieval": decision.should_retrieve}


# ----------------------------
# 2. Direct Answer Generation (No retrieval)
# ----------------------------
def generate_direct(state: State):
    output = llm.invoke(
        direct_generation_prompt.format_messages(
            question=state["question"]
        )
    )
    return {"answer": output.content}


# ----------------------------
# 3. Retrieval
# ----------------------------
def retrieve(state: State):
    vector_store = create_embeddings()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    return {"docs": retriever.invoke(state["question"])}


# ----------------------------
# 4. Relevance Filter
# ----------------------------
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


# ----------------------------
# 5. Generate from Context
# ----------------------------
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

# ----------------------------
# 6. No Answer/Docs Found
# ----------------------------
def no_relevant_docs(state: State):
    return {"answer": "No relevant document found.", "context": ""}


# ----------------------------
# 7. IsSUP verify + revise loop
# ----------------------------
issup_llm = llm.with_structured_output(IsSUPDecision)

def is_sup(state: State):
    decision: IsSUPDecision = issup_llm.invoke(
        issup_prompt.format(
            question=state["question"],
            answer=state.get("answer", ""),
            context=state.get("context", "")
        )
    )

    return {"issup": decision.issup, "evidence": decision.evidence}


# ----------------------------
# 7.1 Revise answer if partially/not supported
# ----------------------------
def revise_answer(state: State):
    out = llm.invoke(
        revise_prompt.format_messages(
            question=state["question"],
            answer=state.get("answer", ""),
            context=state.get("context", ""),
        )
    )
    return {
        "answer": out.content,
        "retries": state.get("retries", 0) + 1,
    }


def accept_answer(state: State):
    return {}  # keep answer as-is