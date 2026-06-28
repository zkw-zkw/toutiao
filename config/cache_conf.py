import json
from typing import Any

import redis.asyncio as redis

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0


redis_client = redis.Redis(
    host = REDIS_HOST,
    port = REDIS_PORT,
    db = REDIS_DB,
    decode_responses = True,
    socket_connect_timeout=3,   # 连接超时3秒
    socket_timeout=3
)

async def get_cache(key:str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败,{e}")
        return None




async def get_json_cache(key:str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    except Exception as e:
        print(f"获取json缓存失败,{e}")
        return None





async def set_cache(key:str,value:Any,espire:int = 3600):
    try:
        if isinstance(value,(dict,list)):
            value = json.dumps(value,ensure_ascii=False)
        await redis_client.setex(key,espire,value)
        return True
    except Exception as e:
        print(f"设置缓存失败,{e}")
        return False





