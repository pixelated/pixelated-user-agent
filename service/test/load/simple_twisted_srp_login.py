# simple script that will spin up a simple twisted webserver, that will only do srp login  to a leap provider
# To run, simply type:
# python service/test/load/simple_twisted_srp_login.py  --multi-user -p unstable.pixelated-project.org

## all the arguments for user-agent apply if supplied

import logging
import os
from string import Template

from OpenSSL import SSL
from OpenSSL import crypto

from pixelated.bitmask_libraries.certs import LeapCertificate
from pixelated.bitmask_libraries.config import LeapConfig
from pixelated.bitmask_libraries.provider import LeapProvider
from pixelated.config import arguments
from pixelated.config import logger
from pixelated.config.site import PixelatedSite
from twisted.internet import reactor
from twisted.internet import ssl
from twisted.web.resource import Resource
from twisted.web.static import File
from twisted.internet.task import LoopingCall

from leap.bonafide.session import Session
from leap.bonafide import provider
from leap.bonafide._http import httpRequest
from leap.srp_session import SRPSession
import json
from twisted.web.http import UNAUTHORIZED, OK
from twisted.cred import credentials
from twisted.web.server import NOT_DONE_YET
from theseus._tracer import Tracer
from pixelated.support.clock import Clock

log = logging.getLogger(__name__)


def _get_static_folder():
    static_folder = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "web-ui", "app"))
    # this is a workaround for packaging
    if not os.path.exists(static_folder):
        static_folder = os.path.abspath(
            os.path.join(os.path.abspath(__file__), "..", "..", "..", "..", "web-ui", "app"))
    if not os.path.exists(static_folder):
        static_folder = os.path.join('/', 'usr', 'share', 'pixelated-user-agent')
    return static_folder


static_folder = _get_static_folder()
_html_template = open(os.path.join(static_folder, 'index.html')).read()
template_response = Template(_html_template).safe_substitute(account_email='ayoyo@ayo.yo')

login_template = '''<html><body>
    <form class="standard" id="login_form" action="/login" method="post">
        <input type="text" name="username" id="email" class="text-field" placeholder="username" tabindex="1"
               autofocus="" />
        <input type="password" name="password" id="password" class="text-field" placeholder="password"
               tabindex="2" autocomplete="off" />
        <input type="submit" name="login" value="Login" class="button" tabindex="3" />
    </form>
</body></html>
'''


class LoginResource(Resource):
    def __init__(self, provider):
        Resource.__init__(self)
        self._leap_provider = provider

    def getChild(self, path, request):
        return self

    def render_GET(self, request):
        request.setResponseCode(OK)
        return login_template

    def render_POST(self, request):
        tl = Clock('naval login user: %s' % request.args['username'][0])

        def render_response(_):
            request.setResponseCode(OK)
            request.write('success!')
            tl.stop()
            request.finish()

        def render_error(error):
            log.info('Login Error for %s' % request.args['username'][0])
            log.info('%s' % error)
            request.setResponseCode(UNAUTHORIZED)
            request.write('Invalid credentials')
            request.finish()

        d = self._handle_login(request)
        d.addCallbacks(render_response, render_error)

        return NOT_DONE_YET

    def _handle_login(self, request):
        _credentials = self._get_creds_from(request)
        srp_provider = provider.Api(self._leap_provider.api_uri)
        srp_auth = Session(_credentials, srp_provider, self._leap_provider.local_ca_crt)

        def srp_session(user_attribute):
            return SRPSession(_credentials.username, srp_auth.token, srp_auth.uuid, 'session_id',
                              json.loads(user_attribute))

        def fetch_attribute(_):
            uri = srp_auth._api._get_uri('update_user', uid=srp_auth._uuid)
            attributes = httpRequest(srp_auth._agent, uri, method='GET')
            attributes.addCallback(srp_session)
            return attributes

        auth = srp_auth.authenticate()
        auth.addCallback(fetch_attribute)
        # auth.addErrback(throw_unauthorized)
        # auth.addCallback(_get_leap_session)
        return auth

    def _get_creds_from(self, request):
        username = request.args['username'][0]
        password = request.args['password'][0]
        return credentials.UsernamePassword(username, password)


class RootResource(Resource):
    def __init__(self, provider):
        Resource.__init__(self)
        self._leap_provider = provider

    def getChild(self, path, request):
        if path == 'login':
            return LoginResource(self._leap_provider)
        return self

        # return File(os.path.join(static_folder, 'index.html'))

    def render_GET(self, request):
        return str(template_response)


class Watchdog:
    def __init__(self, delay=0.01):
        self.delay = delay
        self.loop_call = LoopingCall.withCount(self.watch)

    def start(self):
        self.loop_call.start(self.delay)

    def watch(self, count):
        if count > 1:
            log.info('Reactor was blocked for %s seconds' % (count * self.delay))

    def stop(self):
        return self.loop_call.stop()


def _ssl_options(sslkey, sslcert):
    with open(sslkey) as keyfile:
        pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, keyfile.read())
    with open(sslcert) as certfile:
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, certfile.read())

    acceptable = ssl.AcceptableCiphers.fromOpenSSLCipherString(
        u'ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:!RC4:HIGH:!MD5:!aNULL:!EDH')
    options = ssl.CertificateOptions(privateKey=pkey,
                                     certificate=cert,
                                     method=SSL.TLSv1_2_METHOD,
                                     acceptableCiphers=acceptable)
    return options


def initialize():
    args = arguments.parse_user_agent_args()
    logger.init(debug=args.debug)
    config, provider = initialize_leap_provider(args.provider, args.leap_provider_cert,
                                                args.leap_provider_cert_fingerprint, args.leap_home)
    resource = RootResource(provider)
    dog = Watchdog()
    t = Tracer(reactor)

    def start():
        dog.start()
        t.install()
        start_site(args, resource)
        reactor.getThreadPool().adjustPoolsize(5, 15)

    def stop():
        dog.stop()
        with open('/tmp/callgrind.theseus', 'wb') as outfile:
            t.write_data(outfile)

    reactor.callWhenRunning(start)
    reactor.addSystemEventTrigger('before', 'shutdown', stop)
    reactor.run()


def initialize_leap_provider(provider_hostname, provider_cert, provider_fingerprint, leap_home):
    LeapCertificate.set_cert_and_fingerprint(provider_cert,
                                             provider_fingerprint)

    config = LeapConfig(leap_home=leap_home, start_background_jobs=True)
    provider = LeapProvider(provider_hostname, config)
    provider.download_certificate()
    LeapCertificate(provider).setup_ca_bundle()

    return config, provider


def start_site(config, resource):
    if config.sslkey and config.sslcert:
        reactor.listenSSL(config.port, PixelatedSite(resource), _ssl_options(config.sslkey, config.sslcert),
                          interface=config.host)
    else:
        reactor.listenTCP(config.port, PixelatedSite(resource), interface=config.host)


if __name__ == '__main__':
    initialize()
