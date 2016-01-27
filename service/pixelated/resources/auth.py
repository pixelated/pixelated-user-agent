#
# Copyright (c) 2016 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.

import logging

from leap.auth import SRPAuth
from leap.exceptions import SRPAuthenticationError
from twisted.cred.checkers import ANONYMOUS
from twisted.cred.credentials import ICredentials
from twisted.cred.error import UnauthorizedLogin
from twisted.internet import defer, threads
from twisted.web._auth.wrapper import UnauthorizedResource
from twisted.web.error import UnsupportedMethod
from zope.interface import implements, implementer, Attribute
from twisted.cred import portal, checkers, credentials
from twisted.web import util
from twisted.cred import error
from twisted.web.resource import IResource, ErrorPage

from pixelated.adapter.welcome_mail import add_welcome_mail
from pixelated.config.leap import authenticate_user
from pixelated.config import services
from pixelated.resources import IPixelatedSession


log = logging.getLogger(__name__)


@implementer(checkers.ICredentialsChecker)
class LeapPasswordChecker(object):
    credentialInterfaces = (
        credentials.IUsernamePassword,
        credentials.IUsernameHashedPassword
    )

    def __init__(self, leap_provider):
        self._leap_provider = leap_provider

    def requestAvatarId(self, credentials):
        def _validate_credentials():
            try:
                srp_auth = SRPAuth(self._leap_provider.api_uri, self._leap_provider.local_ca_crt)
                srp_auth.authenticate(credentials.username, credentials.password)
            except SRPAuthenticationError:
                raise UnauthorizedLogin()

        def _authententicate_user(_):
            return authenticate_user(self._leap_provider, credentials.username, credentials.password)

        d = threads.deferToThread(_validate_credentials)
        d.addCallback(_authententicate_user)
        return d


class ISessionCredential(ICredentials):

    request = Attribute('the current request')


@implementer(ISessionCredential)
class SessionCredential(object):
    def __init__(self, request):
        self.request = request


@implementer(checkers.ICredentialsChecker)
class SessionChecker(object):
    credentialInterfaces = (ISessionCredential,)

    def requestAvatarId(self, credentials):
        session = self.get_session(credentials.request)
        if session.is_logged_in():
            return defer.succeed(session.user_uuid)
        else:
            return defer.succeed(ANONYMOUS)

    def get_session(self, request):
        return IPixelatedSession(request.getSession())


class LeapUser(object):

    def __init__(self, leap_session):
        self.leap_session = leap_session


class PixelatedRealm(object):
    implements(portal.IRealm)

    def __init__(self, root_resource, anonymous_resource):
        self._root_resource = root_resource
        self._anonymous_resource = anonymous_resource

    def requestAvatar(self, avatarId, mind, *interfaces):
        if IResource in interfaces:
            if avatarId == checkers.ANONYMOUS:
                return IResource, checkers.ANONYMOUS, lambda: None
            else:
                leap_session = avatarId
                user = LeapUser(leap_session)
                return IResource, user, lambda: None
        raise NotImplementedError()


@implementer(IResource)
class PixelatedAuthSessionWrapper(object):

    isLeaf = False

    def __init__(self, portal, root_resource, anonymous_resource, credentialFactories):
        self._portal = portal
        self._credentialFactories = credentialFactories
        self._root_resource = root_resource
        self._anonymous_resource = anonymous_resource

    def render(self, request):
        raise UnsupportedMethod(())

    def getChildWithDefault(self, path, request):
        request.postpath.insert(0, request.prepath.pop())

        return self._authorizedResource(request)

    def _authorizedResource(self, request):
        creds = SessionCredential(request)
        return util.DeferredResource(self._login(creds))

    def _login(self, credentials):
        d = self._portal.login(credentials, None, IResource)
        d.addCallbacks(self._loginSucceeded, self._loginFailed)
        return d

    def _loginSucceeded(self, args):
        interface, avatar, logout = args

        if avatar == checkers.ANONYMOUS:
            return self._anonymous_resource
        else:
            return self._root_resource

    def _loginFailed(self, result):
        if result.check(error.Unauthorized, error.LoginFailed):
            return UnauthorizedResource(self._credentialFactories)
        else:
            log.err(
                result,
                "HTTPAuthSessionWrapper.getChildWithDefault encountered "
                "unexpected error")
            return ErrorPage(500, None, None)
