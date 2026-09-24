from fastapi import FastAPI

from pydantic import BaseModel

from orchestrator.graph import build_orchestrator


app = FastAPI(
    title="Infineon Multi-Agent Orchestrator"
)


orchestrator = (
    build_orchestrator()
)


class QueryRequest(BaseModel):

    query: str


@app.get("/health")
async def health():

    return {
        "status": "healthy"
    }


@app.post("/chat")
async def chat(
    request: QueryRequest
):

    result = await orchestrator.ainvoke({

        "user_query":
            request.query

    })

    return {

        "answer":
            result["final_answer"],

        "plan":
            result["plan"].model_dump(),

        "agent_results":
            result["results"]
    }

