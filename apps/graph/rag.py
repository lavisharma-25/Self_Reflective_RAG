from langgraph.graph import StateGraph, START, END
from ..schema.schema import State
from .routers import *
from .nodes import *

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
graph.add_node("no_relevant_docs", no_relevant_docs)
graph.add_node("is_sup", is_sup)
graph.add_node("revise_answer", revise_answer)
graph.add_node("accept_answer", accept_answer)

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

graph.add_edge("generate_direct", END)
graph.add_edge("retrieve", "is_relevant")
graph.add_conditional_edges(
    "is_relevant", route_after_relevance,
    {
        "generate_from_context": "generate_from_context",
        "no_relevant_docs": "no_relevant_docs"
    },
)
graph.add_edge("no_relevant_docs", END)
graph.add_edge("generate_from_context", "is_sup")
graph.add_conditional_edges(
    "is_sup", route_after_issup,
    {
        "accept_answer": "accept_answer",
        "revise_answer": "revise_answer"
    }
)
graph.add_edge("revise_answer", "is_sup")
graph.add_edge("accept_answer", END)

workflow = graph.compile()

flow = workflow.get_graph()
png_bytes = flow.draw_mermaid_png()
with open("workflow.png", "wb") as f:
    f.write(png_bytes)