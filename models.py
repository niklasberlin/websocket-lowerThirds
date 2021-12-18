from datetime import datetime, timedelta
from typing import List, Mapping, Optional

from pydantic import BaseModel


class LowerThirdEntry(BaseModel):
    first_line: str
    second_line: Optional[str]
    delay: int = 5000


class TalkEntry(BaseModel):
    name: str
    start: datetime
    duration: timedelta
    lower_thirds: List[str]

class Storage(BaseModel):
    talks: Mapping[str, TalkEntry]
    lower_thirds: Mapping[str, LowerThirdEntry]
    version: str
