from pydantic import BaseModel, Field

from typing import List


class Task(BaseModel):

    id: str

    agent: str

    instruction: str

    depends_on: List[str] = Field(
        default_factory=list
    )


class ExecutionPlan(BaseModel):

    tasks: List[Task]