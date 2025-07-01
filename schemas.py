# schemas.py

from pydantic import BaseModel

# --- Item Schemas ---
class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    # 【重要修正】Pydantic V2 的推荐写法
    class Config:
        from_attributes = True

# --- User Schemas ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    # 【重要修正】Pydantic V2 的推荐写法
    class Config:
        from_attributes = True

# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None