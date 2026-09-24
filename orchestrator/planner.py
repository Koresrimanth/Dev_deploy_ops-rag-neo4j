from langchain_groq import ChatGroq

from langchain_core.prompts import (
    ChatPromptTemplate
)

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

async def create_plan(
    user_query: str
):

    agent_descriptions = (
        get_agent_descriptions()
    )

    prompt = ChatPromptTemplate.from_messages([

        (
            "system",
            """
You are the execution planner for
an enterprise multi-agent system.

Available agents:

{agents}

Your responsibility is to create an
execution plan for the user's query.

Rules:

1. Use only the available agents.

2. If one agent is sufficient,
   create one task.

3. If multiple agents are needed and
   they are independent, they must have
   empty depends_on lists.

4. If one task needs the output of
   another task, add the previous task's
   ID to depends_on.

5. Do not answer the question.

6. Do not call agents.

7. Only create the execution plan.

Return an ExecutionPlan.
"""
        ),

        (
            "human",
            """
User query:

{query}
"""
        )
    ])

    structured_llm = (
        llm.with_structured_output(
            ExecutionPlan
        )
    )

    chain = (
        prompt
        | structured_llm
    )

    plan = await chain.ainvoke({

        "agents":
            agent_descriptions,

        "query":
            user_query
    })

    return plan

