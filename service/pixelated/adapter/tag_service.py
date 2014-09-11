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
from pixelated.adapter.tag import Tag
from pixelated.adapter.tag_index import TagIndex


class TagService:

    instance = None
    SPECIAL_TAGS = {Tag('inbox', True), Tag('sent', True), Tag('drafts', True), Tag('trash', True)}

    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = TagService()
        return cls.instance

    def __init__(self, tag_index=TagIndex()):
        self.tag_index = tag_index

    def load_index(self, mails):
        if self.tag_index.empty():
            for mail in mails:
                self.notify_tags_updated(mail.tags, [], mail.ident)
        for tag in self.SPECIAL_TAGS:
            self.tag_index.add(tag)

    def notify_tags_updated(self, added_tags, removed_tags, mail_ident):
        for removed_tag in removed_tags:
            tag = self.tag_index.get(removed_tag)
            tag.decrement(mail_ident)
            if tag.total == 0:
                self.tag_index.remove(tag.name)
            else:
                self.tag_index.set(tag)
        for added_tag in added_tags:
            tag = self.tag_index.get(added_tag) or self.tag_index.add(Tag(added_tag))
            tag.increment(mail_ident)
            self.tag_index.set(tag)

    def all_tags(self):
        return self.tag_index.values().union(self.SPECIAL_TAGS)
