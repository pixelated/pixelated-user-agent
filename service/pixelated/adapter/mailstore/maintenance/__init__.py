#
# Copyright (c) 2015 ThoughtWorks, Inc.
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
from leap.keymanager.keys import KEY_TYPE_KEY, KEY_PRIVATE_KEY, KEY_ID_KEY, KEY_ADDRESS_KEY
from leap.keymanager.openpgp import OpenPGPKey

from twisted.internet import defer
import logging


TYPE_OPENPGP_KEY = 'OpenPGPKey'
TYPE_OPENPGP_ACTIVE = 'OpenPGPKey-active'

KEY_DOC_TYPES = {TYPE_OPENPGP_ACTIVE, TYPE_OPENPGP_KEY}

logger = logging.getLogger(__name__)


def _is_key_doc(doc):
    return doc.content.get(KEY_TYPE_KEY, None) in KEY_DOC_TYPES


def _is_private_key_doc(doc):
    return _is_key_doc(doc) and doc.content.get(KEY_PRIVATE_KEY, False)


def _is_active_key_doc(doc):
    return _is_key_doc(doc) and doc.content.get(KEY_TYPE_KEY, None) == TYPE_OPENPGP_ACTIVE


def _is_public_key(doc):
    return _is_key_doc(doc) and not doc.content.get(KEY_PRIVATE_KEY, False)


def _key_id(doc):
    return doc.content.get(KEY_ID_KEY, None)


def _address(doc):
    return doc.content.get(KEY_ADDRESS_KEY, None)


class SoledadMaintenance(object):
    def __init__(self, soledad):
        self._soledad = soledad

    @defer.inlineCallbacks
    def repair(self):
        _, docs = yield self._soledad.get_all_docs()

        private_key_ids = self._key_ids_with_private_key(docs)

        for doc in docs:
            if _is_key_doc(doc) and _key_id(doc) not in private_key_ids:
                logger.warn('Deleting doc %s for key %s of <%s>' % (doc.doc_id, _key_id(doc), _address(doc)))
                yield self._soledad.delete_doc(doc)

        yield self._repair_missing_active_docs(docs, private_key_ids)

    @defer.inlineCallbacks
    def _repair_missing_active_docs(self, docs, private_key_ids):
        missing = self._missing_active_docs(docs, private_key_ids)
        for key_id in missing:
            emails = self._emails_for_key_id(docs, key_id)
            for email in emails:
                logger.warn('Re-creating active doc for key %s, email %s' % (key_id, email))
                yield self._soledad.create_doc_from_json(OpenPGPKey(email, key_id=key_id, private=False).get_active_json(email))

    def _key_ids_with_private_key(self, docs):
        return [doc.content[KEY_ID_KEY] for doc in docs if _is_private_key_doc(doc)]

    def _missing_active_docs(self, docs, private_key_ids):
        active_doc_ids = self._active_docs_for_key_id(docs)

        return set([private_key_id for private_key_id in private_key_ids if private_key_id not in active_doc_ids])

    def _emails_for_key_id(self, docs, key_id):
        for doc in docs:
            if _is_private_key_doc(doc) and _key_id(doc) == key_id:
                email = _address(doc)
                if isinstance(email, list):
                    return email
                else:
                    return [email]

    def _active_docs_for_key_id(self, docs):
        return [doc.content[KEY_ID_KEY] for doc in docs if _is_active_key_doc(doc) and _is_public_key(doc)]
