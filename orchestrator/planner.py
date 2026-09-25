from langchain_groq import ChatGroq

from langchain_core.prompts import (
    ChatPromptTemplate
)
import logging
import time
from config.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

from orchestrator.schemas import ExecutionPlan

from orchestrator.registry import AGENT_REGISTRY

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


def get_agent_descriptions():

    descriptions = []

    for name, info in AGENT_REGISTRY.items():

        descriptions.append(
            f"""
Agent name: {name}

Capabilities:
{', '.join(info["capabilities"])}
"""
        )

    return "\n".join(
        descriptions
    )


def get_agent_descriptions():

    descriptions = []

    for name, info in AGENT_REGISTRY.items():

        descriptions.append(
            f"""
Agent: {name}

Capabilities:
{", ".join(info["capabilities"])}
"""
        )

    return "\n".join(descriptions)


async def create_plan(
    request_id: str,
    user_query: str
    
):

    logger.info(
        f"[{request_id}] Planning started"
    )

    agent_descriptions = get_agent_descriptions()
    print(agent_descriptions)
    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
You are an execution planner.

The following agents are available:

{agents}

Create an execution plan for the user's query.

Rules:

1. Select agents ONLY from the available agents.

2. Use the agent capabilities to decide which
   agent should handle each part of the query.

3. If one agent is sufficient, create one task.

4. If multiple agents are required and their work
   is independent, create separate tasks with:

   depends_on = []

5. Use depends_on only when one task requires
   the result of another task.

6. Preserve entity names exactly as provided
   by the user.

   For example:
   IMX-450 must remain IMX-450.

7. Never replace entities with numbers,
   indexes, placeholders, or generic names.

8. Task instructions must contain the actual
   entity from the user's query.

9. If an available agent can handle the query,
   create at least one task.

10. Do not answer the user's question.

11. Return only the ExecutionPlan.
"""
        ),

        (
            "human",
            "{query}"
        )
    ])

    structured_llm = llm.with_structured_output(
        ExecutionPlan
    )

    chain = prompt | structured_llm

    plan = await chain.ainvoke({
        "agents": agent_descriptions,
        "query": user_query
    })

    if not plan.tasks:
        raise ValueError(
            "Planner returned an empty plan"
        )

    for task in plan.tasks:

        if task.agent not in AGENT_REGISTRY:
            raise ValueError(
                f"Unknown agent: {task.agent}"
            )

    logger.info(
        f"[{request_id}] Plan generated | "
        f"tasks={len(plan.tasks)}"
    )

    return plan