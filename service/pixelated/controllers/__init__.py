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


def respond_json(entity, request, status_code=200):
    json_response = json.dumps(entity)
    request.responseHeaders.addRawHeader(b"content-type", b"application/json")
    request.code = status_code
    return json_response


def respond_json_deferred(entity, request, status_code=200):
    json_response = json.dumps(entity)
    request.responseHeaders.addRawHeader(b"content-type", b"application/json")
    request.code = status_code
    request.write(json_response)
    request.finish()


import json

from home_controller import HomeController
from mails_controller import MailsController
from tags_controller import TagsController
from features_controller import FeaturesController
from sync_info_controller import SyncInfoController
from attachments_controller import AttachmentsController
from contacts_controller import ContactsController
