import logging

from aiohttp.web import Response

from sources.base.handlers import BaseView
from sources.base.utils import auth_required
from sources.notification.repository import NotificationRepository
from sources.notification.schemas import Notification
from sources.base.utils import serialize_response, get_response_template
from sources.constants import REQUEST_SENT_INFO, OK_CODE


logger = logging.getLogger(__name__)


class NotificationHandler(BaseView):
    repository = NotificationRepository()
    schema = Notification
    allowed_methods = ('OPTIONS', 'GET', 'POST')

    @auth_required
    async def get(self):
        response = get_response_template()
        registry = await self._get_registry()
        response['rows'] = registry
        logger.info(
            REQUEST_SENT_INFO.format(
                path=self.request.rel_url, status=OK_CODE, method='GET'
            )
        )
        return Response(body=serialize_response(response))
