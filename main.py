# 1. 从 fastapi 库中导入 FastAPI 类
# 这个类是创建所有 API 功能的核心
from fastapi import FastAPI

# 2. 创建一个 FastAPI 应用实例
# 这个实例 `app` 将是我们整个 API 的主要交互对象
app = FastAPI()


# 3. 定义一个“路径操作” (Path Operation)
# `@app.get("/")` 是一个“装饰器 (decorator)”，它告诉 FastAPI：
# 下面这个函数 `read_root` 将会处理所有指向路径 "/" 的 GET 请求。
# - @app: 表示这是由我们的 app 实例管理的
# - .get: 表示这个端点响应的是 HTTP GET 方法
# - "/": 表示路径，根路径，也就是网站的主页地址
@app.get("/")
def read_root():
    # 4. 路径操作函数 (Path Operation Function)
    # 当用户访问 "/" 路径时，这个函数将被调用。
    # FastAPI 会自动将函数返回的 Python 字典或列表转换为 JSON 格式。
    # JSON 是目前网络数据交换最主流的格式。
    return {"message": "你好，世界！欢迎来到 FastAPI 的世界！"}

# 5. 定义一个带路径参数的动态路径
# 这里的 `{item_id}` 是一个“路径参数”，意味着这个部分是动态的。
# 比如用户可以访问 /items/5 或者 /items/abc
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    # a. FastAPI 会自动将路径中的 item_id 作为参数传给函数。
    # `item_id: int` 是 Python 的类型提示，FastAPI 会用它来做数据转换和校验。
    # 如果用户访问 /items/foo，由于 foo 不是整数，FastAPI 会自动返回一个清晰的错误。
    
    # b. `q: str | None = None` 定义了一个可选的“查询参数” q。
    # 意味着用户可以访问 /items/5?q=somequery
    # 如果用户没有提供 q，它的值就是 None。
    
    # c. 函数返回一个包含接收到的参数的字典
    return {"item_id": item_id, "q": q}