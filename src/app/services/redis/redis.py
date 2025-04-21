import redis
import os
from dotenv import load_dotenv

load_dotenv()

redis_ip = os.getenv("REDIS_IP")
redis_port = int(os.getenv("REDIS_PORT"))

# Conectar ao Redis
redis_client = redis.Redis(host=redis_ip, port=redis_port, db=0, decode_responses=True)