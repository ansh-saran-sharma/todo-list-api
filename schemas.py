from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Item(BaseModel):
    title: str
    is_complete: bool = False

class  OutItem(BaseModel):
    title: str
    is_complete: bool
    created_at: datetime

    class Config:
        # This will tell Pydantic Model to read the data even if it is not dictionary, but an orm (SQLAlchemy) Model
        # Absence of this wil cause error -- "value is not a valid dict"
        orm_mode = True