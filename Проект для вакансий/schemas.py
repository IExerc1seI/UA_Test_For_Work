from pydantic import BaseModel
from typing import Optional

class WorkInDB(BaseModel):
    id: int
    Work_name: str
    Salary: str
    City: str
    Info: str

    class Config:
        from_attributes = True

class JobSearchRequest(BaseModel):
    Work_name: Optional[str] = None
    Salary: Optional[str] = None
    City: Optional[str] = "Чернігів"
