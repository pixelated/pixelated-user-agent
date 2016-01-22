from pixelated.resources import BaseResource
from twisted.web import util

from pixelated.resources.login_resource import LoginResource


class LogoutResource(BaseResource):
    BASE_URL = "logout"
    isLeaf = True

    def render_GET(self, request):
        session = self.get_session(request)
        session.expire()
        return util.redirectTo("/%s" % LoginResource.BASE_URL, request)
