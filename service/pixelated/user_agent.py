import json
import datetime
import dateutil.parser as dateparser

from flask import Flask
from flask import request
from flask import Response

import pixelated.reactor_manager as reactor_manager
import pixelated.search_query as search_query
from pixelated.adapter.mail_service import MailService
from pixelated.adapter.pixelated_mail import PixelatedMail
from pixelated.tags import Tags

app = Flask(__name__, static_url_path='', static_folder='../../web-ui/app')

mail_service = MailService()
account = None


def respond_json(entity):
    response = json.dumps(entity)
    return Response(response=response, mimetype="application/json")


@app.route('/disabled_features')
def disabled_features():
    return respond_json([
        'saveDraft',
        'replySection',
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
    raw_mail = json.parse(request.json)
    ident = mail_service.update_mail(raw_mail)
    return respond_json({'ident': ident})


@app.route('/mails')
def mails():
    query = search_query.compile(request.args.get("q")) if request.args.get("q") else {'tags': {}}

    mails = mail_service.mails(query)

    if "inbox" in query['tags']:
        mails = [mail for mail in mails if not mail.has_tag('trash')]

    mails = sorted(mails, key=lambda mail: mail.date, reverse=True)

    mails = [mail.as_dict() for mail in mails]

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
    tags = mail_service.all_tags()
    return respond_json(tags.as_dict())


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
    reactor_manager.start_reactor()
    app.config.from_envvar('PIXELATED_UA_CFG')
    account = app.config['ACCOUNT']
    app.run(host=app.config['HOST'], debug=app.config['DEBUG'], port=app.config['PORT'])


if __name__ == '__main__':
    setup()
