# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取数据库连接 URL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 创建 SQLAlchemy 引擎
# 引擎是 SQLAlchemy 与数据库沟通的核心接口
# connect_args 是只针对 SQLite 的配置，对于 PostgreSQL 我们不需要它
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# 创建一个数据库会话 (Session) 类
# sessionmaker 是一个会话工厂，autocommit=False 和 autoflush=False 是标准配置，
# 确保数据只有在显式调用 commit() 时才被写入数据库。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建一个基础模型类 (Base)
# 我们之后创建的所有数据库模型（数据表）都将继承这个类
Base = declarative_base()