
from pydantic import BaseModel, ConfigDict 
from typing import List, Optional
from datetime import datetime


class TagBase(BaseModel):
    name: str

class ContentBase(BaseModel):
    title: str
    url: str
    description: Optional[str] = None

class TagCreate(TagBase):
    pass

class ContentCreate(ContentBase):
    pass

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
class Tag(TagBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class Content(ContentBase):
    id: int
    owner_id: int
    created_at: datetime
    tags: List[Tag] = []

    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    id: int
    email: str
    full_name : Optional[str] = None
    created_at: datetime
    content: List[Content] = []
    followed_tags: List[Tag] = []
 
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None