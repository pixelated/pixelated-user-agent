from email.utils import parseaddr
from leap.keymanager import OpenPGPKey
from pixelated.resources import respond_json_deferred
from twisted.internet.threads import deferToThread
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
        d = deferToThread(lambda: self._keymanager.get_key_from_cache(key_to_find, OpenPGPKey))
        d.addCallback(finish_request)
        d.addErrback(key_not_found)

        return server.NOT_DONE_YET
