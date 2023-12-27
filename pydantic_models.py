from pydantic import BaseModel, Field


class TaskIn(BaseModel):
    title: str = Field(max_length=32)
    description: str=Field(max_length=128)
    status: bool

class TaskOut(TaskIn):
    id: int
