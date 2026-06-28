from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.news import Category, News


#获取新闻分类列表
async def get_categories(db:AsyncSession,skip:int = 0,limit:int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

#获取新闻列表
async def get_news_list(db:AsyncSession,category_id:int,skip:int = 0,limit:int = 100):
    stmt = select(News).where(News.category_id==category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

#获取某分类下新闻数量
async def get_news_count(db:AsyncSession,category_id:int):
    stmt = select(func.count(News.id)).where(News.category_id==category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

#获取新闻内容
async def get_news_detail(db:AsyncSession,news_id:int):
    stmt = select(News).where(News.id==news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

#增加浏览量
async def increase_news_views(db:AsyncSession,news_id:int):
    stmt = update(News).where(News.id == news_id).values(views = News.views+1)
    result = await db.execute(stmt)
    return result.rowcount > 0

#获取相关新闻的列表
async def get_related_news(db:AsyncSession,news_id:int,category_id:int,limit:int = 5):
    stmt = select(News).where(      #查询条件:分类相同,但不为自己
        News.category_id == category_id,
        News.id != news_id
    ).order_by(                #按浏览量和发布时间降序排序
        News.views.desc(),
        News.publish_time.desc()
    ).limit(limit)              #限制只有limit条
    result = await db.execute(stmt)
    return result.scalars().all()
