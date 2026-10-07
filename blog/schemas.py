from typing import List, Optional
from pydantic import BaseModel

# Used when creating a Blog
class Blog(BaseModel):
    title: str
    body: str

# Used when creating a User
class User(BaseModel):
    name: str
    email: str
    password: str

# Minimal user info to be shown in a blog
class UserBase(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True

# Blog to be shown (includes nested user)
class ShowBlog(BaseModel):
    title: str
    body: str
    creator: UserBase

    class Config:
        orm_mode = True

# Blog summary to be used in user schema (to avoid full circular nesting)
class BlogBase(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True

# User to be shown (includes list of their blogs)
class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[BlogBase]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
