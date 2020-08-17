from conf.settings import *

DATA_COLLECTION_CLEAN_CACHE = ""

caches.set_config({
    'default': {
        'cache': "aiocache.RedisCache",
        'endpoint': "",
        'db': 13,
        'password': "",
        'serializer': {
            'class': "aiocache.serializers.JsonSerializer"
        }
    }
})