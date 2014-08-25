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
from flask import Flask, request, Response, redirect
from factory import MailConverterFactory, ClientFactory
from search import SearchQuery

import json
import datetime
import requests

app = Flask(__name__, static_url_path='', static_folder='../../web-ui/app')
client = None
converter = None
account = None


def from_iso8061_to_date(iso8061):
    return datetime.datetime.strptime(iso8061, "%Y-%m-%dT%H:%M:%S")


def respond_json(entity):
    response = json.dumps(entity)
    return Response(response=response, mimetype="application/json")


@app.route('/mails', methods=['POST'])
def save_draft_or_send():
    ident = None
    if 'sent' in request.json['tags']:
        ident = client.send_draft(converter.to_mail(request.json, account))
    else:
        ident = client.save_draft(converter.to_mail(request.json, account))
    return respond_json({'ident': ident})


@app.route('/mails', methods=['PUT'])
def update_draft():
    ident = client.save_draft(converter.to_mail(request.json, account))
    return respond_json({'ident': ident})


@app.route('/mails')
def mails():
    query = SearchQuery.compile(request.args.get("q"))
    mails = client.drafts() if "drafts" in query['tags'] else client.mails(query)
    mails = [converter.from_mail(mail) for mail in mails]

    if "inbox" in query['tags']:
        mails = [mail for mail in mails if (lambda mail: "trash" not in mail['tags'])(mail)]

    mails = sorted(mails, key=lambda mail: mail['header']['date'], reverse=True)

    response = {
        "stats": {
            "total": len(mails),
            "read": 0,
            "starred": 0,
            "replied": 0
        },
        "mails": mails
    }

    return respond_json(response)


@app.route('/mail/<mail_id>', methods=['DELETE'])
def delete_mails(mail_id):
    client.delete_mail(mail_id)
    return respond_json(None)


@app.route('/tags')
def tags():
    tags = map(lambda x: converter.from_tag(x), client.all_tags())
    return respond_json(tags)


@app.route('/mail/<mail_id>')
def mail(mail_id):
    mail = client.mail(mail_id)
    return respond_json(converter.from_mail(mail))


@app.route('/mail/<mail_id>/tags')
def mail_tags(mail_id):
    mail = converter.from_mail(client.mail(mail_id))
    return respond_json(mail['tags'])


@app.route('/mail/<mail_id>/read', methods=['POST'])
def mark_mail_as_read(mail_id):
    client.mark_as_read(mail_id)
    return ""


@app.route('/contacts')
def contacts():
    query = SearchQuery.compile(request.args.get("q"))
    desired_contacts = [converter.from_contact(contact) for contact in client.all_contacts(query)]
    return respond_json({'contacts': desired_contacts})


@app.route('/draft_reply_for/<mail_id>')
def draft_reply_for(mail_id):
    draft = client.draft_reply_for(mail_id)
    if draft:
        return respond_json(converter.from_mail(draft))
    else:
        return respond_json(None)


@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.config.from_envvar('PIXELATED_SERVICE_CFG')
    provider = app.config['PROVIDER']
    account = app.config['ACCOUNT']

    client = ClientFactory.create(provider, account)
    converter = MailConverterFactory.create(provider, client)
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])
