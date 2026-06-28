from fastapi import APIRouter,Depends,Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud import news, news_cache
from config.database_conf import get_db



#创建一个APIrouter实例 router
router = APIRouter(prefix="/api/news",tags=["news"])    #定义前缀和标题

#创建一个分类列表的路由
@router.get("/categories")
async def get_categories(skip:int = 0,limit:int = 100,db:AsyncSession = Depends(get_db)):
    categories = await news_cache.get_categories(db,skip,limit)
    return {
        "code":200,
        "message":"获取分类列表成功",
        "data":categories
    }

#创建一个新闻列表的路由
@router.get("/list")
async def get_news_list(
        category_id:int= Query(..., alias="categoryId"),
        page:int = 1,
        page_size:int = Query(default=10,le = 100,alias="pageSize"),
        db:AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    news_list = await news_cache.get_news_list(db,category_id,offset,page_size)
    total = await news.get_news_count(db,category_id)
    has_more = (offset + len(news_list)) < total

    return {
        "code":200,
        "message":"获取新闻列表成功",
        "data":{
            "list":news_list,
            "total":total,
            "hasMore":has_more
        }
    }

#创建一个新闻内容的路由
@router.get("/detail")
async def get_news_detail(news_id:int = Query(alias="id"),db:AsyncSession = Depends(get_db)):

    news_detail = await news_cache.get_news_detail(db,news_id)
    if not news_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")

    views_res = await news.increase_news_views(db,news_detail.id)
    if not views_res:
        raise HTTPException(status_code=404, detail="浏览量更新失败")

    related_news = await news_cache.get_related_news(db,news_detail.id,news_detail.category_id)

    return {
        "code":200,
        "message":"success",
        "data":{
            "id":news_detail.id,
            "title":news_detail.title,
            "content":news_detail.content,
            "image":news_detail.image,
            "author":news_detail.author,
            "publishTime":news_detail.publish_time,
            "categoryId":news_detail.category_id,
            "views":news_detail.views,
            "relatedNews":related_news
        }
    }


