import logging

from sources.user.schemas import User, UserUpdate
from sources.user.repositories import UserRepository
from sources.base.handlers import BaseView


logger = logging.getLogger(__name__)


# TODO: Добавить получение реестра пользователей
# TODO: Добавить PATCH запрос к юзеру, с возможность обновления email
class UserDetailHandler(BaseView):
    repository = UserRepository()
    schema = User
    allowed_methods = ('OPTIONS', 'GET', 'PUT', 'DELETE')

    async def put(self):
        self.schema = UserUpdate
        return await super().put()


class UserHandler(UserDetailHandler):
    # TODO: Add hashing password
    allowed_methods = ('OPTIONS', 'POST')
