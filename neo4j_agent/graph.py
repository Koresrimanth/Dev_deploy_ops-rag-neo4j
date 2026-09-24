from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)
from neo4j_agent.nodes import (
    answer_node,
    execute_query_node,
    generate_cypher_node
)

class GraphState(TypedDict, total=False):

    query: str

    cypher: str

    db_result: list

    answer: str


def build_graph():

    builder = StateGraph(
        GraphState
    )

    builder.add_node(
        "generate_cypher",
        generate_cypher_node
    )

    builder.add_node(
        "execute_query",
        execute_query_node
    )

    builder.add_node(
        "answer",
        answer_node
    )

    builder.add_edge(
        START,
        "generate_cypher"
    )

    builder.add_edge(
        "generate_cypher",
        "execute_query"
    )

    builder.add_edge(
        "execute_query",
        "answer"
    )

    builder.add_edge(
        "answer",
        END
    )

    return builder.compile()