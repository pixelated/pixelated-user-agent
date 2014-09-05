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
import json
import argparse
import os
import sys
import os.path
from flask import Flask
from flask import request
from flask import Response
from pixelated.adapter.pixelated_mail_sender import PixelatedMailSender
from pixelated.adapter.pixelated_mailboxes import PixelatedMailBoxes
import pixelated.reactor_manager as reactor_manager
import pixelated.search_query as search_query
import pixelated.bitmask_libraries.session as LeapSession
from pixelated.bitmask_libraries.config import LeapConfig
from pixelated.bitmask_libraries.provider import LeapProvider
from pixelated.bitmask_libraries.auth import LeapAuthenticator, LeapCredentials
from pixelated.adapter.mail_service import MailService
from pixelated.adapter.pixelated_mail import PixelatedMail
import getpass

static_folder = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "web-ui", "app"))

# this is a workaround for packaging
if not os.path.exists(static_folder):
    static_folder = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "web-ui", "app"))
app = Flask(__name__, static_url_path='', static_folder=static_folder)


def respond_json(entity):
    response = json.dumps(entity)
    return Response(response=response, mimetype="application/json")


@app.route('/disabled_features')
def disabled_features():
    return respond_json([
        'saveDraft',
        'draftReply',
        'signatureStatus',
        'encryptionStatus',
        'contacts'
    ])


@app.route('/mails', methods=['POST'])
def send_mail():
    mail = PixelatedMail.from_dict(request.json)
    mail_service.send(mail)
    return respond_json(None)


@app.route('/mails', methods=['PUT'])
def update_draft():
    raw_mail = json.parse(request.json)
    ident = mail_service.update_mail(raw_mail)
    return respond_json({'ident': ident})


@app.route('/mails')
def mails():
    query = search_query.compile(request.args.get("q")) if request.args.get("q") else {'tags': {}}

    mails = mail_service.mails(query)

    if "inbox" in query['tags']:
        mails = [mail for mail in mails if not mail.has_tag('trash')]

    response = {
        "stats": {
            "total": len(mails),
            "read": 0,
            "starred": 0,
            "replied": 0
        },
        "mails": [mail.as_dict() for mail in mails]
    }

    return respond_json(response)


@app.route('/mail/<mail_id>', methods=['DELETE'])
def delete_mails(mail_id):
    mail_service.delete_mail(mail_id)
    return respond_json(None)


@app.route('/tags')
def tags():
    tags = mail_service.all_tags()
    return respond_json([tag.as_dict() for tag in tags])


@app.route('/mail/<mail_id>')
def mail(mail_id):
    mail = mail_service.mail(mail_id)
    return respond_json(mail.as_dict())


@app.route('/mail/<mail_id>/tags', methods=['POST'])
def mail_tags(mail_id):
    new_tags = request.get_json()['newtags']
    tags = mail_service.update_tags(mail_id, new_tags)
    tag_names = [tag.name for tag in tags]
    return respond_json(tag_names)


@app.route('/mail/<mail_id>/read', methods=['POST'])
def mark_mail_as_read(mail_id):
    mail_service.mark_as_read(mail_id)
    return ""


@app.route('/contacts')
def contacts():
    pass


@app.route('/draft_reply_for/<mail_id>')
def draft_reply_for(mail_id):
    pass


@app.route('/')
def index():
    return app.send_static_file('index.html')


def register_new_user(username):
    server_name = app.config['LEAP_SERVER_NAME']
    certs_home = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "certificates"))
    config = LeapConfig(certs_home=certs_home)
    provider = LeapProvider(server_name, config)
    password = getpass.getpass('Please enter password for %s: ' % username)
    LeapAuthenticator(provider).register(LeapCredentials(username, password))
    session = LeapSession.open(username, password, server_name)
    session.nicknym.generate_openpgp_key()


def start_user_agent(debug_enabled):
    leap_session = LeapSession.open(app.config['LEAP_USERNAME'], app.config['LEAP_PASSWORD'],
                                    app.config['LEAP_SERVER_NAME'])
    pixelated_mailboxes = PixelatedMailBoxes(leap_session.account)
    pixelated_mail_sender = PixelatedMailSender(leap_session.account_email())

    global mail_service
    mail_service = MailService(pixelated_mailboxes, pixelated_mail_sender)

    app.run(host=app.config['HOST'], debug=debug_enabled,
            port=app.config['PORT'], use_reloader=False)


def setup():
    try:
        parser = argparse.ArgumentParser(description='Pixelated user agent.')
        parser.add_argument('--debug', action='store_true',
                            help='DEBUG mode.')
        parser.add_argument('--register', metavar='username', help='register user with name.')

        args = parser.parse_args()
        debug_enabled = args.debug or os.environ.get('DEBUG', False)
        reactor_manager.start_reactor(logging=debug_enabled)
        app.config.from_pyfile(os.path.join(os.environ['HOME'], '.pixelated'))

        if args.register:
            register_new_user(args.register)
        else:
            start_user_agent(debug_enabled)
    finally:
        reactor_manager.stop_reactor_on_exit()

if __name__ == '__main__':
    setup()
