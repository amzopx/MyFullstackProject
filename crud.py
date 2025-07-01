# crud.py

from sqlalchemy.orm import Session
# --- 【重要修正】 ---
# 将原来的相对导入 from . import models, schemas
# 改为从项目根目录出发的绝对导入
import models
import schemas
import auth

# --- Item CRUD (保持不变) ---
def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump()) # 使用 Pydantic V2 的 model_dump()
    db.session.add(db_item)
    db.session.commit()
    db.session.refresh(db_item)
    return db_item


# --- User CRUD ---
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    # 使用 auth.py 中的函数来哈希密码
    hashed_password = auth.get_password_hash(user.password)
    # 创建数据库模型实例
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    return db_user