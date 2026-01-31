from pydantic import BaseModel, ConfigDict

class DepartmentBase(BaseModel):
    name: str

class DepartmentResponse(DepartmentBase):
    name: str

    model_config = ConfigDict(from_attributes=True)

