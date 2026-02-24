from apps.graph.rag import workflow

input_data = {
    # "question": "Who is the CEO of NexaAI",
    "question": 'How many employees does NexaAI have?',
    # "question": "What is Machine Learning",
    "need_retrieval": False,
    "docs": [],
    "answer": "",
}
# How many employees does NexaAI have?
# Describe NexaAI’s company culture.
# Do NexaAI plans include a free trial? If yes, how many days?
result = workflow.invoke(input_data)

print("need_retrieval:", result.get("need_retrieval"))
print("#docs:", len(result.get("docs", [])))
print("#relevant_docs:", len(result.get("relevant_docs", [])))
print("issup:", result.get("issup"))
print("evidence:", result.get("evidence"))
print("answer:", result.get("answer"))


for doc in result['docs']:
    print("DOC:\n",doc.page_content)
    print("*"*100)

for doc in result['relevant_docs']:
    print("RELEVANT:\n", doc.page_content)
    print("*"*100)