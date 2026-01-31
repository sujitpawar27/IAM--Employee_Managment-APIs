from pydantic import BaseModel, ConfigDict
from .department_schema import DepartmentResponse
from typing import Optional

class UserCreate(BaseModel):
    name: str
    role: str
    email: str
    department_id: Optional[int] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    department_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    department: DepartmentResponse | None

    model_config = ConfigDict(from_attributes=True)
