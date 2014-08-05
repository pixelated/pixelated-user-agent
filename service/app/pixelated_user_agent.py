import sys
import os
import json
import datetime
import requests

sys.path.insert(0, os.environ['APP_ROOT'])

from flask import Flask, request, Response
from search import SearchQuery
from adapter.mail_service import MailService
from adapter.mail_converter import MailConverter

app = Flask(__name__)
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
    mails = mail_service.drafts() if "drafts" in query['tags'] else mail_service.mails(query)
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


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def redirect_to_front(path):
    response = requests.get("http://localhost:9000/%s" % path)
    return Response(
        response=response,
        status=response.status_code,
        content_type=response.headers['content-type']
    )

if __name__ == '__main__':
    app.config.from_envvar('PIXELATED_UA_CFG')
    account = app.config['ACCOUNT']

    mail_service = MailService()
    converter = MailConverter(mail_service)
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])
