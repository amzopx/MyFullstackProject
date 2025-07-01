# main.py

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta

import crud, models, schemas, auth
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- 依赖项 (Dependency) ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 【新增】获取当前用户的依赖项 ---
async def get_current_user(token: str = Depends(auth.oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except auth.JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# --- 认证路由 (Authentication Routes) ---

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 验证用户名和密码
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 创建 Access Token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# --- 用户路由 (User Routes) ---

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    # 这个端点受 get_current_user 依赖保护，只有携带有效 Token 的请求才能访问
    # FastAPI 会自动处理 Token 的提取和验证
    return current_user

# --- Item 路由 (【重要修改】添加保护) ---

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    # 新增了 current_user 依赖，现在创建 item 也需要登录
    return crud.create_item(db=db, item=item)

@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # 这个端点我们暂时保持公开，任何人都可以查看
    items = crud.get_items(db, skip=skip, limit=limit)
    return items