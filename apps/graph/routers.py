from ..schema.schema import State
from typing import Literal
from logs import setup_logger

logger = setup_logger()

def route_after_decide(state: State) -> Literal["generate_direct", "retrieve"]:
    if state["need_retrieval"]:
        logger.info(f"Routing to 'retrieve' - need_retrieval is True")
        return "retrieve"
    logger.info(f"Routing to 'generate_direct' - need_retrieval is False")
    return "generate_direct"


def route_after_relevance(state: State) -> Literal["generate_from_context", "no_relevant_docs"]:
    if state.get("relevant_docs") and len(state["relevant_docs"]) > 0:
        logger.info(f"Routing to 'generate_from_context' - found {len(state['relevant_docs'])} relevant docs")
        return "generate_from_context"
    logger.info(f"Routing to 'no_relevant_docs' - no relevant docs found")
    return "no_relevant_docs"


MAX_RETRIES = 5

def route_after_issup(state:State) -> Literal["accept_answer", "revise_answer"]:
    if state.get("issup") == "fully_supported":
        logger.info(f"Routing to 'accept_answer' - issup is 'fully_supported'")
        return "accept_answer"
    
    # stop if we've already tried enough
    if state.get("retries", 0) >= MAX_RETRIES:
        logger.info(f"Routing to 'accept_answer' - max retries ({MAX_RETRIES}) reached")
        return "accept_answer"   # or return a "give_up" node if you want

    # otherwise revise again
    logger.info(f"Routing to 'revise_answer' - issup: {state.get('issup')}, retries: {state.get('retries', 0)}")
    return "revise_answer"


def route_after_isuse(state: State) -> Literal["useful", "not_useful"]:
    if state.get("isuse") == "useful":
        logger.info(f"Routing to 'useful' - isuse is 'useful'")
        return "useful"
    logger.info(f"Routing to 'not_useful' - isuse: {state.get('isuse')}")
    return "not_useful"
