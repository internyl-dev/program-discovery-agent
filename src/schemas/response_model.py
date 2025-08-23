
from typing import Literal
from pydantic import BaseModel, HttpUrl

class Output(BaseModel):
    programs: list[HttpUrl]