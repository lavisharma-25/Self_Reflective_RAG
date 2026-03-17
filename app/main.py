from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.health_router import router as health_router
from app.api.index_router import router as index_router
from app.api.doc_router import router as doc_router
from app.api.chat_router import router as chat_router

app = FastAPI(title="Self Reflective RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="static")

app.include_router(index_router)
app.include_router(health_router)
app.include_router(doc_router)
app.include_router(chat_router)









# from app.graph.rag import workflow

# # -----------------------------
# # Run the graph
# # -----------------------------
# initial_state = {
#     "question": "Where is IBM?",
#     # "retrieval_query": "What is the refund policy of NexaAI",
#     # "question": "What is machine learning?",
#     "rewrite_max_retries": 0,
#     "docs": [],
#     "relevant_docs": [],
#     "context": "",
#     "answer": "",
#     "issup": "",
#     "evidence": [],
#     "retries": 0,
#     "isuse": "not_useful",
#     "use_reason": "",
# }


# result = workflow.invoke(
#     initial_state,
#     config={"recursion_limit": 80},  # allow revise → verify loops
# )

# # -----------------------------
# # Debug / inspection output (clean + complete)
# # -----------------------------
# print("\n===== RAG EXECUTION RESULT =====\n")

# print("Question:", initial_state.get("question"))
# print("Need Retrieval:", result.get("need_retrieval"))

# # If you added these counters/fields in your State:
# print("Rewrite tries (retrieval):", result.get("rewrite_max_retries", 0))
# print("Support revise tries:", result.get("retries", 0))

# print("\nRetrieval:")
# print("  Total retrieved docs:", len(result.get("docs", []) or []))
# print("  Relevant docs:", len(result.get("relevant_docs", []) or []))

# # Optional: show sources/pages for relevant docs
# relevant_docs = result.get("relevant_docs", []) or []
# if relevant_docs:
#     print("\nRelevant docs (source/page):")
#     for i, d in enumerate(relevant_docs, 1):
#         src = (d.metadata or {}).get("source", "unknown")
#         page = (d.metadata or {}).get("page", None)
#         title = (d.metadata or {}).get("title", "")
#         extra = f", title={title}" if title else ""
#         if page is not None:
#             print(f"  {i}. source={src}, page={page}{extra}")
#         else:
#             print(f"  {i}. source={src}{extra}")

# print("\nVerification (IsSUP):")
# print("  issup:", result.get("issup"))
# evidence = result.get("evidence", []) or []
# if evidence:
#     print("  evidence:")
#     for e in evidence:
#         print("   -", e)
# else:
#     print("  evidence: (none)")

# print("\nUsefulness (IsUSE):")
# print("  isuse:", result.get("isuse"))
# print("  reason:", result.get("use_reason", ""))

# print("\nFinal Answer:")
# print(result.get("answer"))

# print("\n===============================\n")