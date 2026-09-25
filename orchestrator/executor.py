from orchestrator.registry import AGENT_REGISTRY
import logging
import time
import asyncio
import httpx
from typing import Dict, Any
from config.logger import setup_logging
setup_logging()
logger = logging.getLogger(__name__)



async def call_agent(
    agent_name: str,
    payload: dict,
    request_id: str,
    task_id: str
):
    start_time = time.perf_counter()
    logger.info(
        f"[{request_id}] Agent call started | "
        f"task={task_id} | "
        f"agent={agent_name}"
    )

    agent = AGENT_REGISTRY.get(
        agent_name
    )

    if agent is None:

        raise ValueError(
            f"Unknown agent: {agent_name}"
        )
    try:

        async with httpx.AsyncClient(
            timeout=60
        ) as client:

            response = await client.post(
                agent["url"],
                json=payload
            )

            response.raise_for_status()
            result = response.json()
            latency = (
                time.perf_counter() - start_time
            )

            logger.info(
                f"[{request_id}] Agent call completed | "
                f"task={task_id} | "
                f"agent={agent_name} | "
                f"status={response.status_code} | "
                f"latency={latency:.3f}s"
            )

            return response.json()
        
    except httpx.TimeoutException as e:

        logger.exception(
            f"[{request_id}] Agent timeout | "
            f"task={task_id} | "
            f"agent={agent_name}"
        )

    except httpx.ConnectError as e:

        logger.exception(
            f"[{request_id}] Agent connection failed | "
            f"task={task_id} | "
            f"agent={agent_name}"
        )


def build_input(
    task,
    results,
    request_id: str
) -> dict:

    # --------------------------------------------------------
    # No dependencies
    # --------------------------------------------------------

    if not task.depends_on:

        logger.info(
            f"[{request_id}] "
            f"Building independent task input | "
            f"task={task.id}"
        )

        return {
            "query": task.instruction
        }

    # --------------------------------------------------------
    # Task has dependencies
    # --------------------------------------------------------

    previous_results = []

    for dependency in task.depends_on:

        dependency_result = results.get(dependency)

        if dependency_result is None:

            raise RuntimeError(
                f"Dependency '{dependency}' "
                f"result not found"
            )

        # ----------------------------------------------------
        # Dependency failed
        # ----------------------------------------------------

        if dependency_result.get("status") != "success":

            raise RuntimeError(
                f"Dependency '{dependency}' "
                f"did not complete successfully"
            )

        previous_results.append(
            dependency_result["data"]
        )

    logger.info(
        f"[{request_id}] "
        f"Building dependent task input | "
        f"task={task.id} | "
        f"dependencies={task.depends_on}"
    )

    return {
        "query": task.instruction,
        "previous_results": previous_results
    }

async def run_task(
    task,
    results: Dict[str, Any],
    request_id: str
):

    start_time = time.perf_counter()

    logger.info(
        f"[{request_id}] "
        f"Task execution started | "
        f"task={task.id} | "
        f"agent={task.agent} | "
        f"dependencies={task.depends_on}"
    )

    try:

        # ----------------------------------------------------
        # Build request payload
        # ----------------------------------------------------

        payload = build_input(
            task=task,
            results=results,
            request_id=request_id
        )

        logger.info(
            f"[{request_id}] "
            f"Calling agent | "
            f"task={task.id} | "
            f"agent={task.agent}"
        )

        # ----------------------------------------------------
        # Call remote agent
        # ----------------------------------------------------

        output = await call_agent(
            agent_name=task.agent,
            payload=payload,
            request_id=request_id,
            task_id=task.id
        )

        latency = time.perf_counter() - start_time

        logger.info(
            f"[{request_id}] "
            f"Task completed | "
            f"task={task.id} | "
            f"agent={task.agent} | "
            f"latency={latency:.3f}s"
        )

        return {
            "status": "success",
            "data": output,
            "latency": latency
        }

    except Exception as e:

        latency = time.perf_counter() - start_time

        logger.exception(
            f"[{request_id}] "
            f"Task failed | "
            f"task={task.id} | "
            f"agent={task.agent} | "
            f"latency={latency:.3f}s | "
            f"error={str(e)}"
        )

        return {
            "status": "failed",
            "error": str(e),
            "error_type": type(e).__name__,
            "latency": latency
        }


# ============================================================
# Check whether dependency failed
# ============================================================

def dependency_failed(
    task,
    results: Dict[str, Any]
) -> bool:

    for dependency in task.depends_on:

        dependency_result = results.get(
            dependency
        )

        if dependency_result is None:
            return False

        if dependency_result["status"] != "success":
            return True

    return False




################################      Main code             ###########################################################


async def execute_plan(
    plan,
    request_id: str
):

    logger.info(
        f"[{request_id}] "
        f"Execution started | "
        f"total_tasks={len(plan.tasks)}"
    )

    results: Dict[str, Any] = {}

    completed = set()

    # --------------------------------------------------------
    # Create task lookup
    # --------------------------------------------------------

    tasks = {
        task.id: task
        for task in plan.tasks
    }

    # --------------------------------------------------------
    # Validate task IDs
    # --------------------------------------------------------

    if len(tasks) != len(plan.tasks):

        raise RuntimeError(
            "Duplicate task IDs found in execution plan"
        )

    # ========================================================
    # Execution loop
    # ========================================================

    while len(completed) < len(tasks):

        ready_tasks = []

        # ----------------------------------------------------
        # Find tasks that can execute
        # ----------------------------------------------------

        for task in plan.tasks:

            # Already completed
            if task.id in completed:
                continue

            # ------------------------------------------------
            # Check dependencies
            # ------------------------------------------------

            dependencies_ready = all(
                dependency in completed
                for dependency in task.depends_on
            )

            if dependencies_ready:

                ready_tasks.append(task)

        # ----------------------------------------------------
        # No task is ready
        # ----------------------------------------------------

        if not ready_tasks:

            logger.error(
                f"[{request_id}] "
                f"No executable tasks found"
            )

            raise RuntimeError(
                "No ready tasks found. "
                "Possible circular dependency."
            )

        # ----------------------------------------------------
        # Log ready tasks
        # ----------------------------------------------------

        logger.info(
            f"[{request_id}] "
            f"Ready tasks: "
            f"{[task.id for task in ready_tasks]}"
        )

        # ====================================================
        # Handle dependency failures
        # ====================================================

        executable_tasks = []

        for task in ready_tasks:

            if dependency_failed(
                task,
                results
            ):

                logger.error(
                    f"[{request_id}] "
                    f"Task blocked because dependency failed | "
                    f"task={task.id} | "
                    f"dependencies={task.depends_on}"
                )

                results[task.id] = {
                    "status": "blocked",
                    "error": (
                        "One or more dependencies "
                        "failed"
                    )
                }

                completed.add(task.id)

            else:

                executable_tasks.append(task)

        # ====================================================
        # Execute ready tasks in parallel
        # ====================================================

        if executable_tasks:

            logger.info(
                f"[{request_id}] "
                f"Executing tasks in parallel | "
                f"tasks="
                f"{[task.id for task in executable_tasks]}"
            )

            outputs = await asyncio.gather(
                *[
                    run_task(
                        task=task,
                        results=results,
                        request_id=request_id
                    )
                    for task in executable_tasks
                ]
            )

            # ------------------------------------------------
            # Store results
            # ------------------------------------------------

            for task, output in zip(
                executable_tasks,
                outputs
            ):

                results[task.id] = output

                completed.add(task.id)

                logger.info(
                    f"[{request_id}] "
                    f"Task result stored | "
                    f"task={task.id} | "
                    f"status={output['status']}"
                )

    # ========================================================
    # Execution finished
    # ========================================================

    logger.info(
        f"[{request_id}] "
        f"Execution completed successfully"
    )

    return results