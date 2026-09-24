import os

from dotenv import load_dotenv


load_dotenv()


AGENT_REGISTRY = {

    "rag_agent": {

        "url": (
            os.getenv("RAG_AGENT_URL")
            + "/invoke_rag"
        ),

        "capabilities": [
            "technical documentation",
            "component specifications",
            "operating temperature",
            "input voltage",
            "technical manuals",
            "unstructured document retrieval"
        ]
    },

    "graph_agent": {

        "url": (
            os.getenv("GRAPH_AGENT_URL")
            + "/invoke_graph"
        ),

        "capabilities": [
            "supplier relationships",
            "component relationships",
            "supplier dependencies",
            "product relationships",
            "multi-hop graph traversal"
        ]
    }
}