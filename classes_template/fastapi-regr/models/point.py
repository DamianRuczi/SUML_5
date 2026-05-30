from pydantic import BaseModel
from typing import Optional

class Point(BaseModel):
    x: float
    y: Optional[float]