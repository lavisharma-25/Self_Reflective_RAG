from apps.graph.rag import workflow

input_data = {
        "question": "Describe NexaAI’s company culture.",
        "docs": [],
        "relevant_docs": [],
        "context": "",
        "answer": "",
        "issup": "",
        "evidence": [],
        "retries": 0,
    }

result = workflow.invoke(input_data)

print("need_retrieval:", result.get("need_retrieval"))
print("#docs:", len(result.get("docs", [])))
print("#relevant_docs:", len(result.get("relevant_docs", [])))
print("issup:", result.get("issup"))
print("evidence:", result.get("evidence"))
print("answer:", result.get("answer"))
print("retries:", result.get("retries"))


# for doc in result['docs']:
#     print("DOC:\n",doc.page_content)
#     print("*"*100)

# for doc in result['relevant_docs']:
#     print("RELEVANT:\n", doc.page_content)
#     print("*"*100)