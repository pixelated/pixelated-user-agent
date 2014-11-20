def setup_routes(app, home_controller, mails_controller, tags_controller, features_controller, sync_info_controller,
                 attachments_controller, contacts_controller):
    # mails
    app.route('/mails', methods=['GET'])(mails_controller.mails)
    app.route('/mail/<mail_id>/read', methods=['POST'])(mails_controller.mark_mail_as_read)
    app.route('/mail/<mail_id>/unread', methods=['POST'])(mails_controller.mark_mail_as_unread)
    app.route('/mails/unread', methods=['POST'])(mails_controller.mark_many_mail_unread)
    app.route('/mails/read', methods=['POST'])(mails_controller.mark_many_mail_read)
    app.route('/mail/<mail_id>', methods=['GET'])(mails_controller.mail)
    app.route('/mail/<mail_id>', methods=['DELETE'])(mails_controller.delete_mail)
    app.route('/mails', methods=['DELETE'])(mails_controller.delete_mails)
    app.route('/mails', methods=['POST'])(mails_controller.send_mail)
    app.route('/mail/<mail_id>/tags', methods=['POST'])(mails_controller.mail_tags)
    app.route('/mails', methods=['PUT'])(mails_controller.update_draft)
    # tags
    app.route('/tags', methods=['GET'])(tags_controller.tags)
    # contacts
    app.route('/contacts', methods=['GET'])(contacts_controller.contacts)
    # features
    app.route('/features', methods=['GET'])(features_controller.features)
    # sync info
    app.route('/sync_info', methods=['GET'])(sync_info_controller.sync_info)
    # attachments
    app.route('/attachment/<attachment_id>', methods=['GET'])(attachments_controller.attachment)
    # static
    app.route('/', methods=['GET'], branch=True)(home_controller.home)