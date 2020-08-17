import logging

import requests
from tenacity import wait_exponential, retry, retry_if_exception_type, stop_after_attempt

from exception import ExternalServerCalledFailure

logger = logging.getLogger('root')


class AuditProcessEventService:
    AUDIT_RESULT_STATUS_PASS = 2
    AUDIT_RESULT_STATUS_REFUSE = 3
    AUDIT_RESULT_STATUS_REAPPLY = 6
    NOTIFY_DATA_COLLECTION_CLEAN_CACHE_PASS = 1
    NOTIFY_DATA_COLLECTION_CLEAN_CACHE_REFUSE = 2
    NOTIFY_DATA_COLLECTION_CLEAN_CACHE_REAPPLY = 3

    NOTIFY_DATA_COLLECTION_CLEAN_CACHE_AUDIT_RESULT_MAP = {
        AUDIT_RESULT_STATUS_PASS: NOTIFY_DATA_COLLECTION_CLEAN_CACHE_PASS,
        AUDIT_RESULT_STATUS_REFUSE: NOTIFY_DATA_COLLECTION_CLEAN_CACHE_REFUSE,
        AUDIT_RESULT_STATUS_REAPPLY: NOTIFY_DATA_COLLECTION_CLEAN_CACHE_REAPPLY
    }

    def __init__(self, event):
        self.event = event
        self.product = self.event['product']
        self.user = self.event['user']

    @retry(wait=wait_exponential(multiplier=1, min=5, max=20),
           stop=stop_after_attempt(15),
           retry=retry_if_exception_type(ExternalServerCalledFailure))
    async def handle_audit_totally_complete(self):
        from event2call_riskdata_app import sanic_app
        result = self.event['result']
        extra = result['extra']

        product = self.product['name']

        data = {
            'product_name': product,
            'product_id': self.product['id'],

        }
        if extra:
            data.update(extra)

        logger.info(f'handle_audit_totally_complete request clean cache api data: {data}')
        response = requests.post(sanic_app.config.DATA_COLLECTION_CLEAN_CACHE, json=data)
        logger.info(f'handle_audit_totally_complete request clean cache api status: {response.status_code}')
        if response.status_code != 200:
            raise ExternalServerCalledFailure(f'response status code:{response.status_code}')
        else:
            logger.info(f'handle_audit_totally_complete request clean cache api response data: {response.json()}')

    @retry(wait=wait_exponential(multiplier=1, min=5, max=20),
           stop=stop_after_attempt(15),
           retry=retry_if_exception_type(ExternalServerCalledFailure))
    async def handle_rule_result(self):
        from event2call_riskdata_app import sanic_app
        rule = self.event['rule']
        if 'idcard' in rule['description']:
            response = requests.post(sanic_app.config.DATA_COLLECTION_CLEAN_CACHE, json={
                'product_id': self.product['id'],
                'apply_id': self.event['history_id'],
                'product_name': self.product['name'],
            })
            logger.info(f'request clean cache api status: {response.status_code}')

            if response.status_code != 200:
                raise ExternalServerCalledFailure(f'response status code:{response.status_code}')
            else:
                logger.info(
                    'request clean cache api(event:high_idcard_event) response data: {}'.format(response.json()))
