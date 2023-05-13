from aiohttp.web import Response

from backend.base.handlers import BaseView
from backend.base.utils import auth_required
from backend.notification.repository import NotificationRepository
from backend.notification.schemas import NotificationSchema
from backend.base.utils import get_response_template, serialize_response
from backend.notification.models import Notification
from backend.constants import NOT_ALLOWED, REQUEST_SENT_INFO, OK_CODE


class NotificationHandler(BaseView):
    repository = NotificationRepository()
    schema = NotificationSchema
    allowed_methods = ('OPTIONS', 'GET', 'POST')
    model = Notification

    @auth_required
    async def get(self):
        if 'GET' not in self.allowed_methods:
            return Response(status=NOT_ALLOWED)
        response = get_response_template()

        registry = await self.repository.get_registry()
        for row in registry:
            row = row['Notification'].__dict__
            del row['_sa_instance_state']
            response['rows'].append(row)

        self.logger.info(
            REQUEST_SENT_INFO.format(
                path=self.request.rel_url, status=OK_CODE, method='GET'
            )
        )
        return Response(body=serialize_response(response))
