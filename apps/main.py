from apps.graph.rag import workflow
import json

input_data = {
    "question": "What is company refund policy?"
    # 'question': "What is Machine Learning?"
}

result = workflow.invoke(input_data)
test = dict(result)
print(f"{result['question']}")
# print(f"{result['answer']}")
print(test.keys())