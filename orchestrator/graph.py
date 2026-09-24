from typing import TypedDict, Any

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from orchestrator.planner import create_plan

from orchestrator.executor import execute_plan


class OrchestratorState(
    TypedDict,
    total=False
):

    user_query: str

    plan: Any

    results: dict

    final_answer: str


from typing import TypedDict, Any

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from .planner import create_plan

from .executor import execute_plan


class OrchestratorState(
    TypedDict,
    total=False
):

    user_query: str

    plan: Any

    results: dict

    final_answer: str


async def planner_node(
    state
):

    plan = await create_plan(
        state["user_query"]
    )

    return {
        "plan": plan
    }

async def executor_node(
    state
):

    results = await execute_plan(
        state["plan"]
    )

    return {
        "results": results
    }


from langchain_groq import ChatGroq


final_llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


async def final_answer_node(
    state
):

    prompt = f"""
You are the final response generator.

User question:

{state["user_query"]}

Results returned by the specialized agents:

{state["results"]}

Create one clear answer using
only these results.

Do not invent information.
"""

    response = await final_llm.ainvoke(
        prompt
    )

    return {
        "final_answer":
            response.content
    }



def build_orchestrator():

    builder = StateGraph(
        OrchestratorState
    )

    builder.add_node(
        "planner",
        planner_node
    )

    builder.add_node(
        "executor",
        executor_node
    )

    builder.add_node(
        "final_answer",
        final_answer_node
    )

    builder.add_edge(
        START,
        "planner"
    )

    builder.add_edge(
        "planner",
        "executor"
    )

    builder.add_edge(
        "executor",
        "final_answer"
    )

    builder.add_edge(
        "final_answer",
        END
    )

    return builder.compile()


