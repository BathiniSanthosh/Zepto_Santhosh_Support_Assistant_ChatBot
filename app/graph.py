import logging

from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    END
)

from rag import retrieve

logger = logging.getLogger(__name__)

logger.info("Loading graph.py")


class GraphState(TypedDict):

    question: str
    answer: str
    sources: list
    confidence: float


def assistant(state):

    logger.info(
        f"Question received: {state['question']}"
    )

    result = retrieve(
        state["question"]
    )

    return {

        "question": state["question"],

        "answer": result["answer"],

        "sources": result["sources"],

        "confidence": result["confidence"]
    }


builder = StateGraph(
    GraphState
)

builder.add_node(
    "assistant",
    assistant
)

builder.set_entry_point(
    "assistant"
)

builder.add_edge(
    "assistant",
    END
)

graph = builder.compile()

logger.info(
    "Graph compiled successfully"
)