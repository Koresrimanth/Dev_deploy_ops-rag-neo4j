import httpx

from orchestrator.registry import AGENT_REGISTRY



# async def call_agent(
#     agent_name: str,
#     payload: dict
# ):

#     agent = AGENT_REGISTRY.get(
#         agent_name
#     )

#     if agent is None:

#         raise ValueError(
#             f"Agent '{agent_name}' not found"
#         )

#     url = agent["url"]

#     async with httpx.AsyncClient(
#         timeout=60
#     ) as client:

#         response = await client.post(
#             url,
#             json=payload
#         )

#         response.raise_for_status()

#         return response.json()

import asyncio
import httpx

# from .registry import AGENT_REGISTRY


async def call_agent(
    agent_name: str,
    payload: dict
):

    agent = AGENT_REGISTRY.get(
        agent_name
    )

    if agent is None:

        raise ValueError(
            f"Unknown agent: {agent_name}"
        )

    async with httpx.AsyncClient(
        timeout=60
    ) as client:

        response = await client.post(
            agent["url"],
            json=payload
        )

        response.raise_for_status()

        return response.json()


def build_input(
    task,
    results
):

    if not task.depends_on:

        return {
            "query": task.instruction
        }

    previous_results = []

    for dependency in task.depends_on:

        previous_results.append(
            results[dependency]
        )

    return {
        "query": task.instruction,

        "previous_results":
            previous_results
    }

async def execute_plan(plan):

    results = {}

    completed = set()

    tasks = {
        task.id: task
        for task in plan.tasks
    }

    while len(completed) < len(tasks):

        ready_tasks = []

        for task in plan.tasks:

            if task.id in completed:
                continue

            if all(
                dep in completed
                for dep in task.depends_on
            ):

                ready_tasks.append(task)

        if not ready_tasks:

            raise RuntimeError(
                "No ready tasks. "
                "Possible circular dependency."
            )

        async def run_task(task):

            payload = build_input(
                task,
                results
            )

            return await call_agent(
                task.agent,
                payload
            )

        outputs = await asyncio.gather(
            *[
                run_task(task)
                for task in ready_tasks
            ]
        )

        for task, output in zip(
            ready_tasks,
            outputs
        ):

            results[task.id] = output

            completed.add(
                task.id
            )

    return results

