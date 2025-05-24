from typing import List
from pydantic import BaseModel


class ConcallData(BaseModel):
  ID: int
  TickerName: str
  Links: List[str]
