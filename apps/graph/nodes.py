from typing import List
from langchain_core.documents import Document
from .prompts import *
from ..model.llm_model import llm
from ..embeddings.vector_store import create_embeddings
from ..schema.schema import *
from langchain_community.tools.tavily_search import TavilySearchResults
from logs import setup_logger

logger = setup_logger()

# ----------------------------
# 1. Decide Retrieval
# ----------------------------
should_retrieve_llm = llm.with_structured_output(RetrieveDecision)

def decide_retrieval(state: "State"):
    question = str(state["question"])
    logger.info(f"Deciding retrieval for question: {question}")
    
    decision: RetrieveDecision = should_retrieve_llm.invoke(
        decide_retrieval_prompt.format_messages(question=question)
    )
    
    logger.info(f"Retrieval decision: {decision.should_retrieve}")
    return {"need_retrieval": decision.should_retrieve}


# ----------------------------
# 2. Direct Answer Generation (No retrieval)
# ----------------------------
def generate_direct(state: State):
    question = state["question"]
    logger.info(f"Generating direct answer for question: {question}")
    
    output = llm.invoke(
        direct_generation_prompt.format_messages(
            question=question
        )
    )
    
    logger.info(f"Direct answer generated: {output.content[:100]}...")
    return {"answer": output.content}


# ----------------------------
# 3. Retrieval
# ----------------------------
def retrieve(state: State):
    vector_store = create_embeddings()
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    question = state.get("rewrite_question") or state["question"]
    
    logger.info(f"Retrieving documents for question: {question}")
    docs = retriever.invoke(question)
    logger.info(f"Retrieved {len(docs)} documents")
    
    return {"docs": docs}


# ----------------------------
# 4. Relevance Filter
# ----------------------------
relevance_llm = llm.with_structured_output(RelevanceDecision)

def is_relevant(state: State):
    relevant_docs: List[Document] = []
    question = state["question"]
    logger.info(f"Checking relevance for question: {question}")

    for i, doc in enumerate(state["docs"]):
        decision: RelevanceDecision = relevance_llm.invoke(
            is_relevant_prompt.format_messages(
                question=question,
                document=doc.page_content
            )
        )

        logger.info(f"Document {i+1} relevance: {decision.is_relevant}")

        if decision.is_relevant:
            relevant_docs.append(doc)

    logger.info(f"Found {len(relevant_docs)} relevant documents out of {len(state['docs'])}")
    return {"relevant_docs": relevant_docs}


# ----------------------------
# 5. Generate from Context
# ----------------------------
def generate_from_context(state: State):
    question = state["question"]
    logger.info(f"Generating answer from context for question: {question}")
    
    # Stuff relevant docs into one block
    context = "\n\n---\n\n".join(
        [d.page_content for d in state.get("relevant_docs", [])]
    ).strip()

    if not context:
        logger.info("No relevant document found for context")
        return {"answer": "No relevant document found.", "context": ""}

    out = llm.invoke(
        rag_generation_prompt.format_messages(
            question=question,
            context=context
        )
    )
    
    logger.info(f"Answer generated from context: {out.content[:100]}...")
    return {"answer": out.content, "context": context}


# ----------------------------
# 6. Rewrite query
# ----------------------------
rewrite_llm = llm.with_structured_output(WebQuery)

def rewrite_query(state: State):
    question = state["question"]
    logger.info(f"Rewriting question: {question}")
    
    out : WebQuery = rewrite_llm.invoke(
        rewrite_prompt.format_messages(question=question)
    )
    
    logger.info(f"Rewritten query: {out.web_query}")
    return {"web_query": out.web_query}


# ----------------------------
# 6.1 Web search with rewritten query
# ----------------------------
tavily = TavilySearchResults(max_results=5)

def web_search(state: State):
    q = state.get("web_query") or state["question"]
    logger.info(f"Performing web search with query: {q}")
    
    results = tavily.invoke({"query": q})

    docs = []
    for r in results or []:
        title = r.get("title", "")
        url = r.get("url", "")
        content = r.get("content", "") or r.get("snippet", "")
        text = f"TITLE: {title}\nURL: {url}\nCONTENT:\n{content}"
        docs.append(
            Document(
                page_content=text,
                metadata={"source": "web", "url": url, "title": title},
            )
        )

    logger.info(f"Web search returned {len(docs)} results")
    return {"docs": docs}


# ----------------------------
# 7. IsSUP verify + revise loop
# ----------------------------
issup_llm = llm.with_structured_output(IsSUPDecision)

def is_sup(state: State):
    question = state["question"]
    answer = state.get("answer", "")
    logger.info(f"Verifying SUP for question: {question}")
    
    decision: IsSUPDecision = issup_llm.invoke(
        issup_prompt.format(
            question=question,
            answer=answer,
            context=state.get("context", "")
        )
    )

    logger.info(f"SUP decision: issup={decision.issup}, evidence={decision.evidence}")
    return {"issup": decision.issup, "evidence": decision.evidence}


# ----------------------------
# 7.1 Revise answer if partially/not supported
# ----------------------------
def revise_answer(state: State):
    question = state["question"]
    logger.info(f"Revising answer for question: {question}")
    
    out = llm.invoke(
        revise_prompt.format_messages(
            question=question,
            answer=state.get("answer", ""),
            context=state.get("context", ""),
        )
    )
    
    logger.info(f"Revised answer: {out.content[:100]}...")
    return {
        "answer": out.content,
        "retries": state.get("retries", 0) + 1,
    }


# ----------------------------
# 8. IsUSE - Decide whether the generated answer is useful or not
# ----------------------------
isuse_llm = llm.with_structured_output(IsUSEDecision)

def is_use(state: State):
    question = state["question"]
    answer = state.get("answer", "")
    logger.info(f"Checking if answer is useful for question: {question}")
    
    decision: IsUSEDecision = isuse_llm.invoke(
        isuse_prompt.format_messages(
            question=question,
            answer=answer,
        )
    )

    logger.info(f"IsUSE decision: isuse={decision.isuse}, reason={decision.reason}")
    return {"isuse": decision.isuse, "use_reason": decision.reason}


# ----------------------------
# 9. Rewrite question if answer not useful
# ----------------------------
rewrite_llm = llm.with_structured_output(RewriteDecision)

def rewrite_question(state: State):
    question = state["question"]
    logger.info(f"Rewriting question for retrieval: {question}")
    
    decision: RewriteDecision = rewrite_llm.invoke(
        rewrite_for_retrieval_prompt.format_messages(
            question=question,
            retrieval_query = state.get("retrieval_query", ""),
            answer=state.get("answer", "")
        )
    )

    logger.info(f"Rewritten retrieval query: {decision.retrieval_query}")
    return {
        "retrieval_query": decision.retrieval_query,
        "rewrite_max_retries": state.get("rewrite_max_retries", 0) + 1,
    }
    