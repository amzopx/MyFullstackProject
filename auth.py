# auth.py

from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

# --- 配置 ---
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# --- 密码哈希 ---
# 创建一个 passlib 上下文，指定使用 bcrypt 算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer 是一个类，它提供了一种从请求中提取 Token 的方式
# tokenUrl="token" 指明了客户端应该向哪个 URL 发送用户名和密码来获取 Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- 函数 ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证明文密码和哈希密码是否匹配"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密码的哈希值"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建 JWT Access Token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 如果没有提供过期时间，则使用默认的15分钟
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    # 使用密钥和算法对数据进行编码，生成 JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt