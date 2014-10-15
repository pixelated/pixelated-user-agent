#
# Copyright (c) 2014 ThoughtWorks, Inc.
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
import argparse
import getpass

import os
import os.path
import crochet
from flask import Flask
from pixelated.adapter.pixelated_mail_sender import PixelatedMailSender
from pixelated.adapter.pixelated_mailboxes import PixelatedMailBoxes
import pixelated.reactor_manager as reactor_manager
import pixelated.bitmask_libraries.session as LeapSession
from pixelated.bitmask_libraries.config import LeapConfig
from pixelated.bitmask_libraries.provider import LeapProvider
from pixelated.bitmask_libraries.auth import LeapAuthenticator, LeapCredentials
from pixelated.adapter.mail_service import MailService
from pixelated.adapter.pixelated_mail import InputMail
from pixelated.adapter.soledad_querier import SoledadQuerier
from pixelated.adapter.search import SearchEngine
from pixelated.adapter.draft_service import DraftService
from pixelated.adapter.listener import MailboxListener
from pixelated.controllers import *
from pixelated.adapter.tag_service import TagService


static_folder = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "web-ui", "app"))
# this is a workaround for packaging
if not os.path.exists(static_folder):
    static_folder = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "web-ui", "app"))
if not os.path.exists(static_folder):
    static_folder = os.path.join('/', 'usr', 'share', 'pixelated-user-agent')

app = Flask(__name__, static_url_path='', static_folder=static_folder)


def register_new_user(username, server_name):
    certs_home = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "certificates"))
    config = LeapConfig(certs_home=certs_home)
    provider = LeapProvider(server_name, config)
    password = getpass.getpass('Please enter password for %s: ' % username)
    LeapAuthenticator(provider).register(LeapCredentials(username, password))
    session = LeapSession.open(username, password, server_name)
    session.nicknym.generate_openpgp_key()


def _setup_routes(app, home_controller, mails_controller, tags_controller, features_controller):
    # home
    app.add_url_rule('/', methods=['GET'], view_func=home_controller.home)
    # mails
    app.add_url_rule('/mails', methods=['GET'], view_func=mails_controller.mails)
    app.add_url_rule('/mail/<mail_id>/read', methods=['POST'], view_func=mails_controller.mark_mail_as_read)
    app.add_url_rule('/mail/<mail_id>/unread', methods=['POST'], view_func=mails_controller.mark_mail_as_unread)
    app.add_url_rule('/mails/unread', methods=['POST'], view_func=mails_controller.mark_many_mail_unread)
    app.add_url_rule('/mail/<mail_id>', methods=['GET'], view_func=mails_controller.mail)
    app.add_url_rule('/mail/<mail_id>', methods=['DELETE'], view_func=mails_controller.delete_mail)
    app.add_url_rule('/mails', methods=['DELETE'], view_func=mails_controller.delete_mails)
    app.add_url_rule('/mails', methods=['POST'], view_func=mails_controller.send_mail)
    app.add_url_rule('/mail/<mail_id>/tags', methods=['POST'], view_func=mails_controller.mail_tags)
    app.add_url_rule('/mails', methods=['PUT'], view_func=mails_controller.update_draft)
    # tags
    app.add_url_rule('/tags', methods=['GET'], view_func=tags_controller.tags)
    # features
    app.add_url_rule('/features', methods=['GET'], view_func=features_controller.features)


def start_user_agent(debug_enabled, app):

    with app.app_context():
        leap_session = LeapSession.open(app.config['LEAP_USERNAME'], app.config['LEAP_PASSWORD'],
                                        app.config['LEAP_SERVER_NAME'])
        tag_service = TagService()
        soledad_querier = SoledadQuerier(soledad=leap_session.account._soledad)
        pixelated_mailboxes = PixelatedMailBoxes(leap_session.account, soledad_querier)
        pixelated_mail_sender = PixelatedMailSender(leap_session.account_email())
        mail_service = MailService(pixelated_mailboxes, pixelated_mail_sender, tag_service, soledad_querier)
        search_engine = SearchEngine()
        search_engine.index_mails(mail_service.all_mails())
        draft_service = DraftService(pixelated_mailboxes)

        MailboxListener.SEARCH_ENGINE = search_engine
        InputMail.FROM_EMAIL_ADDRESS = leap_session.account_email()

        home_controller = HomeController()
        features_controller = FeaturesController()
        mails_controller = MailsController(mail_service=mail_service,
                                           draft_service=draft_service,
                                           search_engine=search_engine)
        tags_controller = TagsController(search_engine=search_engine)

        _setup_routes(app, home_controller, mails_controller, tags_controller, features_controller)

        app.run(host=app.config['HOST'], debug=debug_enabled,
                port=app.config['PORT'], use_reloader=False)


def setup():
    try:
        default_config_path = os.path.join(os.environ['HOME'], '.pixelated')

        parser = argparse.ArgumentParser(description='Pixelated user agent.')
        parser.add_argument('--debug', action='store_true',
                            help='DEBUG mode.')
        parser.add_argument('--register', metavar='username', help='register user with name.')
        parser.add_argument('-c', '--config', metavar='configfile', default=default_config_path,
                            help='use specified config file. Default is ~/.pixelated.')

        args = parser.parse_args()
        debug_enabled = args.debug or os.environ.get('DEBUG', False)
        reactor_manager.start_reactor(logging=debug_enabled)

        crochet.setup()

        app.config.from_pyfile(args.config)

        if args.register:
            server_name = app.config['LEAP_SERVER_NAME']
            register_new_user(args.register, server_name)
        else:
            start_user_agent(debug_enabled, app)
    finally:
        reactor_manager.stop_reactor_on_exit()


if __name__ == '__main__':
    setup()
