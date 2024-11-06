import redis
from django.conf import settings

redis_instance = redis.StrictRedis.from_url(settings.REDIS_URL, decode_responses=True)
