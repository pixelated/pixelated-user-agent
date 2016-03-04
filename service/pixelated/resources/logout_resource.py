from twisted.web.server import NOT_DONE_YET

from pixelated.resources import BaseResource
from twisted.web import util
from twisted.internet import defer

from pixelated.resources.login_resource import LoginResource


class LogoutResource(BaseResource):
    BASE_URL = "logout"
    isLeaf = True

    @defer.inlineCallbacks
    def _execute_logout(self, request):
        session = self.get_session(request)
        yield self._services_factory.log_out_user(session.user_uuid)
        session.expire()

    def render_POST(self, request):
        def _redirect_to_login(_):
            content = util.redirectTo("/%s" % LoginResource.BASE_URL, request)
            request.write(content)
            request.finish()

        d = self._execute_logout(request)
        d.addCallback(_redirect_to_login)

        return NOT_DONE_YET
