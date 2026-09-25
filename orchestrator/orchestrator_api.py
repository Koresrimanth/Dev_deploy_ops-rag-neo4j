from fastapi import FastAPI, HTTPException
import logging
from pydantic import BaseModel
import uuid
from orchestrator.graph import build_orchestrator
logger = logging.getLogger(__name__)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Infineon Multi-Agent Orchestrator"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = (
    build_orchestrator()
)


class QueryRequest(BaseModel):
    request_id:str
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
    request_id = request.request_id
    user_query = request.query
    logger.info(
        f"[{request_id}] Request received | "
        f"query={request.query}"
    )



    try:

        result = await orchestrator.ainvoke({
            "request_id": request_id,
            "user_query":request.query

        })

        return {

        "answer":
            result["final_answer"],

        "plan":
            result["plan"].model_dump(),

        "agent_results":
            result["results"]
        }
    except Exception as e:

        logger.exception(
            f"[{request_id}] Orchestration failed | "
            f"error={str(e)}"
        )
    raise HTTPException(
            status_code=500,
            detail={
                "request_id": request_id,
                "message": "Orchestration failed"
            }
        )


