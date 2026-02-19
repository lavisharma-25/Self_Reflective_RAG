from langchain_core.prompts import ChatPromptTemplate
from prompts import (retrieval_router_prompt, direct_generate_prompt)
from model.llm_model import llm
from schema.schema import State, RetrieveDecision

decide_retrieval_prompt = ChatPromptTemplate.from_messages(retrieval_router_prompt)
should_retrieve_llm = llm.with_structured_output(RetrieveDecision)

def decide_retrieval(state: "State"):
    decision: RetrieveDecision = should_retrieve_llm.invoke(
        decide_retrieval_prompt.format_messages(question=state["question"])
    )
    return {"need_retrieval": decision.should_retrieve}


direct_generation_prompt = ChatPromptTemplate.from_messages(direct_generate_prompt)

def generate_direct(state: State):
    output = llm.invoke(
        direct_generation_prompt.format_messages(
            question=state["question"]
        )
    )
    return {"answer": output.content}

def retrieve(state: State):
    retriever = vector_store_instance.as_retriever(search_kwargs={"k": 4})
    return {"docs": retriever.invoke(state["question"])}