from langgraph.graph import StateGraph, START, END
from ..schema.schema import State
from .routers import (route_after_decide, route_after_relevance)
from .nodes import (
    decide_retrieval, 
    generate_direct, 
    retrieve, 
    is_relevant,
    generate_from_context,
    no_relevant_docs
    )

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
graph.add_edge("generate_from_context", END)
graph.add_edge("no_relevant_docs", END)

workflow = graph.compile()

flow = workflow.get_graph()
png_bytes = flow.draw_mermaid_png()
with open("workflow.png", "wb") as f:
    f.write(png_bytes)