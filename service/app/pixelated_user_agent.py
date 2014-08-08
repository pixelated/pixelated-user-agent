import json
import datetime
import requests

from flask import Flask, request, Response
import app.search_query as search_query
from app.adapter.mail_service import MailService
from app.adapter.mail_converter import MailConverter

app = Flask(__name__, static_url_path='', static_folder='../../web-ui/app')

mail_service = MailService()
converter = MailConverter(mail_service)
account = None


def from_iso8061_to_date(iso8061):
    return datetime.datetime.strptime(iso8061, "%Y-%m-%dT%H:%M:%S")


def respond_json(entity):
    response = json.dumps(entity)
    return Response(response=response, mimetype="application/json")

@app.route('/disabled_features')
def disabled_features():
    return respond_json([
        'saveDraft',
        'createNewTag',
        'replySection',
        'tags',
        'signatureStatus',
        'encryptionStatus',
        'contacts'
    ])


@app.route('/mails', methods=['POST'])
def save_draft_or_send():
    ident = None
    if 'sent' in request.json['tags']:
        ident = mail_service.send_draft(converter.to_mail(request.json, account))
    else:
        ident = mail_service.save_draft(converter.to_mail(request.json, account))
    return respond_json({'ident': ident})


@app.route('/mails', methods=['PUT'])
def update_draft():
    ident = mail_service.save_draft(converter.to_mail(request.json, account))
    return respond_json({'ident': ident})


@app.route('/mails')
def mails():
    query = search_query.compile(request.args.get("q")) if request.args.get("q") else {'tags': {}}
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
    mail_service.delete_mail(mail_id)
    return respond_json(None)


@app.route('/tags')
def tags():
    tags = map(lambda x: converter.from_tag(x), mail_service.all_tags())
    return respond_json(tags)


@app.route('/mail/<mail_id>')
def mail(mail_id):
    mail = mail_service.mail(mail_id)
    return respond_json(converter.from_mail(mail))


@app.route('/mail/<mail_id>/tags')
def mail_tags(mail_id):
    mail = converter.from_mail(mail_service.mail(mail_id))
    return respond_json(mail['tags'])


@app.route('/mail/<mail_id>/read', methods=['POST'])
def mark_mail_as_read(mail_id):
    mail_service.mark_as_read(mail_id)
    return ""


@app.route('/contacts')
def contacts():
    query = search_query.compile(request.args.get("q"))
    desired_contacts = [converter.from_contact(contact) for contact in mail_service.all_contacts(query)]
    return respond_json({'contacts': desired_contacts})


@app.route('/draft_reply_for/<mail_id>')
def draft_reply_for(mail_id):
    draft = mail_service.draft_reply_for(mail_id)
    if draft:
        return respond_json(converter.from_mail(draft))
    else:
        return respond_json(None)


@app.route('/')
def index():
    return app.send_static_file('index.html')


def setup():
    app.config.from_envvar('PIXELATED_UA_CFG')
    account = app.config['ACCOUNT']
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])

if __name__ == '__main__':
    setup()
