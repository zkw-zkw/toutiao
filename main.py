from fastapi import FastAPI
from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handlers import register_exception_handlers


app = FastAPI()

register_exception_handlers(app)

#定义一个允许访问的源的列表
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000"
]

#使用中间件解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    #允许访问的源
    allow_credentials=True,   #允许携带Cookie
    allow_methods=["*"],      #允许所有请求方法
    allow_headers=["*"]       #允许所有请求头
)


@app.get("/")
async def root():
    return {"message": "Hello World"}




#注册routers中的路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)

