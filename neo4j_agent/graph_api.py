from fastapi import FastAPI
from pydantic import BaseModel

from neo4j_agent.graph import build_graph


app = FastAPI(
    title="Infineon Graph Agent"
)

graph = build_graph()


class GraphRequest(BaseModel):

    query: str


@app.post("/invoke_graph")
async def invoke(
    request: GraphRequest
):

    result = await graph.ainvoke({

        "query": request.query

    })

    return {

        "agent": "graph_agent",

        "answer":
            result["answer"],

        "data":
            result["db_result"]
    }