from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

ASYNC_DATABASE_URL="mysql+aiomysql://root:051215@localhost:3306/news_app?charset=utf8mb4"

#创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo = True,            #开启日志
    pool_size = 10,         #最大连接池10
    max_overflow = 20       #可超出20
)

#创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind = async_engine,     #绑定数据库引擎
    class_=AsyncSession,     #指定会话类
    expire_on_commit=False   #提交会话后不过期,不会重新查询数据库
)

#提供依赖注入函数
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session    #返回数据库会话给路由处理函数
            await session.commit()
        except:
            await session.rollback()
            raise
