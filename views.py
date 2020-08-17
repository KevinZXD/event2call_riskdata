# pylint:disable=unused-argument
import logging

from sanic.response import json
from sanic.views import HTTPMethodView

from services import AuditProcessEventService

logger = logging.getLogger('root')


class EventView(HTTPMethodView):
    async def post(self, request, *args, **kwargs):
        try:
            event = request.headers['X-HfaxFK-Event']
            delivery = request.headers['X-HfaxFK-Delivery']
            code_version = request.headers['User-Agent']
            data = request.json
            action = data.get('action')

            if event == 'audit_process' and action == 'rule_result':
                logger.info(
                    f'receive audit_process event, action is rule_result, the delivery: {delivery}, code version: {code_version}')
                await AuditProcessEventService(data).handle_rule_result()

            if event == 'audit_process' and action == 'audit_totally_complete':
                logger.info(
                    f'receive audit_process event, action is audit_totally_complete, the delivery: {delivery}, code version: {code_version}')
                await AuditProcessEventService(data).handle_audit_totally_complete()
        except Exception as e:
            logger.error(f'handle post data error:{e}')
        return json({'action': 'pong'})
