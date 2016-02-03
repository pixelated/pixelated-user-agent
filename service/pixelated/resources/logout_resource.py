from pixelated.resources import BaseResource
from twisted.web import util

from pixelated.resources.login_resource import LoginResource


class LogoutResource(BaseResource):
    BASE_URL = "logout"
    isLeaf = True

    def render_GET(self, request):
        session = self.get_session(request)
        self._services_factory.log_out_user(session.user_uuid)
        session.expire()

        return util.redirectTo("/%s" % LoginResource.BASE_URL, request)
