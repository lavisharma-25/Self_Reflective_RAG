from langgraph.graph import StateGraph, START, END

from app.graph.nodes import *
from app.graph.routers import *
from app.models.state import State


# -----------------------------
# Build graph
# -----------------------------
graph = StateGraph(State)

# --------------------
# Nodes
# --------------------
graph.add_node("decide_retrieval", decide_retrieval)
graph.add_node("generate_direct", generate_direct)
graph.add_node("retrieve", retrieve)
graph.add_node("is_relevant", is_relevant)
graph.add_node("generate_from_context", generate_from_context)
graph.add_node("rewrite_query", rewrite_query)
graph.add_node("web_search", web_search)
graph.add_node("no_relevant_docs", no_relevant_docs)
graph.add_node("is_sup", is_sup)
graph.add_node("revise_answer", revise_answer)
graph.add_node("is_use", is_use)
graph.add_node("rewrite_question", rewrite_question)
graph.add_node("update_history", update_history)

# --------------------
# Edges
# --------------------
graph.add_edge(START, "decide_retrieval")

graph.add_conditional_edges(
    "decide_retrieval", route_after_decide,
    {
        "generate_direct": "generate_direct",
        "retrieve": "retrieve",
    },
)

graph.add_edge("generate_direct", "update_history")
graph.add_edge("retrieve", "is_relevant")
graph.add_conditional_edges(
    "is_relevant", route_after_relevance,
    {
        "generate_from_context": "generate_from_context",
        "no_relevant_docs": "rewrite_query"
    },
)
graph.add_conditional_edges(
    "rewrite_query", route_after_rewrite,
    {
        "web_search": "web_search",
        "no_relevant_docs": "no_relevant_docs"
    }
)
graph.add_edge("no_relevant_docs", "update_history")
graph.add_edge("web_search", "is_use")
graph.add_edge("generate_from_context", "is_sup")
graph.add_conditional_edges(
    "is_sup", route_after_issup,
    {
        "accept_answer": "is_use",
        "revise_answer": "revise_answer"
    }
)
graph.add_edge("revise_answer", "is_sup")
graph.add_conditional_edges("is_use", route_after_isuse,
    {
        "useful": "update_history",
        "not_useful": "rewrite_question"
    }
)

graph.add_edge("update_history", END)
graph.add_edge("rewrite_question", "retrieve")

workflow = graph.compile()

flow = workflow.get_graph()
png_bytes = flow.draw_mermaid_png()
with open("workflow.png", "wb") as f:
    f.write(png_bytes)


from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

store = {}

def get_session_history(session_id: str):

    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]


conversational_chain = RunnableWithMessageHistory(
    workflow,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)