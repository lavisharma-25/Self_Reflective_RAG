from langgraph.graph import StateGraph, START, END
from ..schema.schema import State
from .nodes import (decide_retrieval, generate_direct, retrieve, is_relevant)
from .routers import route_after_decide

graph = StateGraph(State)

# --------------------
# Nodes
# --------------------
graph.add_node("decide_retrieval", decide_retrieval)
graph.add_node("generate_direct", generate_direct)
graph.add_node("retrieve", retrieve)
graph.add_node("is_relevant", is_relevant)

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
graph.add_edge("is_relevant", END)

workflow = graph.compile()

flow = workflow.get_graph()
png_bytes = flow.draw_mermaid_png()
with open("workflow.png", "wb") as f:
    f.write(png_bytes)