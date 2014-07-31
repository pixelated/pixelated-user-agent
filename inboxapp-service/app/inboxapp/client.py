import json
import urllib2
import requests


class Client:

    INBOX_APP_ROOT = 'http://localhost:5555/n'

    def _get_user(self, account):
        accounts = json.load(urllib2.urlopen(self.INBOX_APP_ROOT))
        return [a for a in accounts if a['email_address'] == account][0]

    def __init__(self, account):
        self.user = self._get_user(account)
        self.namespace = self.user['namespace']

    def _get(self, append_url):
        url = "%s/%s/%s" % (self.INBOX_APP_ROOT, self.namespace, append_url)
        return requests.get(url).json()

    def _post(self, append_url, body):
        url = "%s/%s/%s" % (self.INBOX_APP_ROOT, self.namespace, append_url)
        return requests.post(url, json.dumps(body)).json()

    def _put(self, append_url, body):
        url = "%s/%s/%s" % (self.INBOX_APP_ROOT, self.namespace, append_url)
        return requests.put(url, json.dumps(body)).json()

    def mails(self, query):
        url = "messages"
        if('tags' in query and len(query['tags']) > 0):
            url = url + "?tag=%s" % ",".join(query['tags'])
        return self._get(url)

    def drafts(self):
        return self._get("drafts")

    def mail(self, mail_id):
        return self._get("messages/%s" % mail_id)

    def thread(self, thread_id):
        return self._get("threads/%s" % thread_id)

    def mark_as_read(self, mail_id):
        mail_to_mark = self.mail(mail_id)
        self._put("messages/%s" % mail_id, {"unread": False})
        self.remove_tag_from_thread(mail_to_mark["thread"], "unread")

    def tags_for_thread(self, thread):
        url = "threads/%s" % thread
        tags = self._get(url)['tags']
        return [tag['name'] for tag in tags]

    def add_tag_to_thread(self, thread_id, tag):
        url = "threads/%s" % thread_id
        response = self._put(url, {'add_tags': [tag]})
        return response

    def remove_tag_from_thread(self, thread_id, tag):
        url = "threads/%s" % thread_id
        response = self._put(url, {'remove_tags': [tag]})
        return response

    def delete_mail(self, mail_id):
        thread_id = self.mail(mail_id)['thread']
        tags = self.tags_for_thread(thread_id)
        if('trash' in tags):
            self.add_tag_to_thread(thread_id, 'delete')
        else:
            self.add_tag_to_thread(thread_id, 'trash')
        return None

    def save_draft(self, draft):
        if 'id' in draft and draft['id']:
            url = 'drafts/%s' % draft["id"]
        else:
            url = "drafts"
        result = self._post(url, draft)
        self.mark_as_read(result['id'])
        return result['id']

    def send_draft(self, draft):
        new_draft_id = self.save_draft(draft)
        response = self._post("send", {"draft_id": new_draft_id})
        return response

    def draft_reply_for(self, mail_id):
        thread = self.thread(self.mail(mail_id)["thread"])
        if thread['drafts']:
            response = self.mail(thread['drafts'][0])
        else:
            response = None
        return response

    def all_tags(self):
        return self._get("tags")

    def all_contacts(self, query):
        return self._get("contacts?filter=%s&order_by=rank" % query['general'])
