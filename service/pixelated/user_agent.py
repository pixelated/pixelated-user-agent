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
import getpass

import os
import os.path
import crochet
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
from pixelated.adapter.pixelated_mail import PixelatedMail, InputMail
from pixelated.adapter.soledad_querier import SoledadQuerier


static_folder = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "web-ui", "app"))

# this is a workaround for packaging
if not os.path.exists(static_folder):
    static_folder = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", "..", "web-ui", "app"))
if not os.path.exists(static_folder):
    static_folder = os.path.join('/', 'usr', 'share', 'pixelated-user-agent')
app = Flask(__name__, static_url_path='', static_folder=static_folder)
DISABLED_FEATURES = ['draftReply', 'signatureStatus', 'encryptionStatus', 'contacts']


def respond_json(entity, status_code=200):
    json_response = json.dumps(entity)
    response = Response(response=json_response, mimetype="application/json")
    response.status_code = status_code
    return response


@app.route('/disabled_features')
def disabled_features():
    return respond_json(DISABLED_FEATURES)


@app.route('/mails', methods=['POST'])
def send_mail():
    _mail = InputMail.from_dict(request.json)
    draft_id = request.json.get('ident')
    if draft_id:
        mail_service.send(draft_id, _mail)
    else:
        _mail = mail_service.create_draft(_mail)
    return respond_json(_mail.as_dict())


@app.route('/mails', methods=['PUT'])
def update_draft():
    _mail = InputMail.from_dict(request.json)
    new_revision = mail_service.update_draft(request.json['ident'], _mail)
    ident = new_revision.ident
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
def delete_mail(mail_id):
    mail_service.delete_mail(mail_id)
    return respond_json(None)


@app.route('/mails', methods=['DELETE'])
def delete_mails():
    idents = json.loads(request.form['idents'])
    for ident in idents:
        mail_service.delete_mail(ident)
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
    new_tags = map(lambda tag: tag.lower(), request.get_json()['newtags'])
    try:
        tags = mail_service.update_tags(mail_id, new_tags)
    except ValueError as ve:
        return respond_json(ve.message, 403)
    return respond_json(list(tags))


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
    SoledadQuerier.get_instance(soledad=leap_session.account._soledad)
    PixelatedMail.from_email_address = leap_session.account_email()
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

        crochet.setup()
        app.config.from_pyfile(os.path.join(os.environ['HOME'], '.pixelated'))

        if args.register:
            register_new_user(args.register)
        else:
            start_user_agent(debug_enabled)
    finally:
        reactor_manager.stop_reactor_on_exit()

if __name__ == '__main__':
    setup()
