from typing import TypedDict, List
from langgraph.graph import (
    StateGraph,
    START,
    END
)
from rag_agent.nodes import (
    retrieve_node,
    context_node,
    answer_node,
)


class RAGState(TypedDict, total=False):

    query: str

    component_ids: List[str]

    documents: list

    context: str

    sources: list

    answer: str


def build_graph():

    builder = StateGraph(
        RAGState
    )

    builder.add_node(
        "retrieve",
        retrieve_node
    )

    builder.add_node(
        "context",
        context_node
    )

    builder.add_node(
        "answer",
        answer_node
    )

    builder.add_edge(
        START,
        "retrieve"
    )

    builder.add_edge(
        "retrieve",
        "context"
    )

    builder.add_edge(
        "context",
        "answer"
    )

    builder.add_edge(
        "answer",
        END
    )

    return builder.compile()

