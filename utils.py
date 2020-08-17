import logging
import re
import datetime
from conf.settings import caches
from consts import TIMEOUT

logger = logging.getLogger('root')


def get_product_short_name(route_key):
    """
    获取产品名称短名称
    """
    # e.g.  'review_hyuk_1' ==>  'hyuk'
    matched = re.match(r'review_(.+)_\d+', route_key)
    if matched:
        return matched.group(1)
    return route_key


async def call_third_service_limit(key, limit_times, count=1):
    cache = caches.get('default')
    key_related_date = key + datetime.date.today().strftime('%y%m%d')
    await cache.expire(key_related_date, TIMEOUT)
    return (await cache.increment(key_related_date, count)) > limit_times


async def is_call_weixin_service(new_fraud_model_b_score):
    result = False
    if new_fraud_model_b_score is None:
        logger.info('rule_space.new_fraud_model_B_score not exist, not call third service')

    elif 800 < new_fraud_model_b_score < 900:
        logger.info('rule_space.new_fraud_model_B_score not satisfy condition, not call third service')

    elif new_fraud_model_b_score <= 800 and await call_third_service_limit('wx_call_limit_150', 150):
        logger.info('call weixin data third api extend the limit time, not call third service')

    elif new_fraud_model_b_score > 900 and await call_third_service_limit('wx_call_limit_50', 50):
        logger.info('call weixin data third api extend the limit time, not call third service')

    else:
        result = True

    return result
