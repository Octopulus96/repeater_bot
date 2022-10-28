from ctypes.wintypes import WORD
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    word: str
    description: Optional[str] = None
    new_word: Optional[str] = None
    new_description: Optional[str] = None

    class Config:
        orm_mode = True
