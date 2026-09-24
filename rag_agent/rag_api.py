from fastapi import FastAPI
from pydantic import BaseModel

from rag_agent.graph import build_graph


app = FastAPI(
    title="Infineon RAG Agent"
)

rag_graph = build_graph()


class RAGRequest(BaseModel):

    query: str

    component_ids: list[str] = []


@app.post("/invoke_rag")
async def invoke(
    request: RAGRequest
):

    result = await rag_graph.ainvoke({

        "query": request.query,

        "component_ids":
            request.component_ids

    })

    return {
        "agent": "rag_agent",
        "answer": result["answer"],
        "sources": result.get(
            "sources",
            []
        )
    }