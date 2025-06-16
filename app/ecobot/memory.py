# memory.py
import os
from dotenv import load_dotenv
from langgraph.store.redis import RedisStore
from langgraph.checkpoint.redis import RedisSaver

load_dotenv()
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

def get_memory_store():
    return RedisStore.from_conn_string(redis_url)

def get_checkpointer():
    return RedisSaver.from_conn_string(redis_url)
