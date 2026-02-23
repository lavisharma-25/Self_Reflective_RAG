from apps.graph.rag import workflow

input_data = {
    "question": "Who is the CEO of NexaAI",
    "need_retrieval": False,
    "docs": [],
    "answer": "",
}

result = workflow.invoke(input_data)

print(f"Question: {result['question']}")
print(f"Answer: {result['answer']}")
print(f"Bool: {result['need_retrieval']}")
print(f"Docs: {result['docs']}")


for doc in result['docs']:
    print(doc.page_content)
    print("*"*100)

for doc in result['relevant_docs']:
    print(doc.page_content)
    print("*"*100)