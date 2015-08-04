from email.utils import parseaddr
from pixelated.resources import respond_json_deferred
from twisted.web import server
from twisted.web.resource import Resource


class KeysResource(Resource):

    isLeaf = True

    def __init__(self, keymanager):
        Resource.__init__(self)
        self._keymanager = keymanager

    def render_GET(self, request):
        def finish_request(key):
            if key.private:
                respond_json_deferred(None, request, status_code=401)
            else:
                respond_json_deferred(key.get_json(), request)

        def key_not_found(_):
            respond_json_deferred(None, request, status_code=404)

        _, key_to_find = parseaddr(request.args.get('search')[0])
        d = self._keymanager.fetch_key(key_to_find)
        d.addCallback(finish_request)
        d.addErrback(key_not_found)

        return server.NOT_DONE_YET
