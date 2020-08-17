import sys
from aiocache import caches

# cache
caches.set_config({
    'default': {
        'cache': "aiocache.RedisCache",
        'endpoint': "127.0.0.1",
        'db': 1,
        'password': "redispassword",
        'serializer': {
            'class': "aiocache.serializers.JsonSerializer"
        }
    }
})


LOGGING = dict(
    version=1,
    disable_existing_loggers=False,

    loggers={
        "root": {
            "level": "INFO",
            "handlers": ["console"]
        },
        "sanic.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": True,
            "qualname": "sanic.error"
        },
        "sanic.access": {
            "level": "INFO",
            "handlers": ["access_console"],
            "propagate": True,
            "qualname": "sanic.access"
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout
        },
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s]  %(module)s [%(lineno)d] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
        "access": {
            "format": ("%(asctime)s - %(process)d - %(name)s)[%(levelname)s][%(host)s] : "
                       "%(request)s %(message)s %(status)d %(byte)d"),
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
    }
)

DATA_COLLECTION_CLEAN_CACHE = 'http://127.0.0.1:8000/mock/api/data/handle/'
DATA_COLLECTION_URL = "http://127.0.0.1:8000/mock/api/data/collection/"
