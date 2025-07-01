# models.py
from sqlalchemy import Column, Integer, String, Boolean
# --- 【重要修正】 ---
# 将相对导入 from .database import Base
# 改为从项目根目录出发的绝对导入
from database import Base

# Item 模型保持不变
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

# 【新增】User 模型
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    # unique=True 保证了用户名在数据库中是唯一的
    username = Column(String, unique=True, index=True, nullable=False)
    # 存储哈希后的密码，而不是明文密码
    hashed_password = Column(String, nullable=False)
    # 一个简单的字段，用于区分普通用户和管理员
    is_active = Column(Boolean, default=True)