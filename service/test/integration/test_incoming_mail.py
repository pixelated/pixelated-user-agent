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
from pixelated.adapter.listeners.mailbox_indexer_listener import MailboxIndexerListener
from test.support.integration import SoledadTestBase, MailBuilder
from twisted.internet import defer, reactor

IGNORED = None


class IncomingMailTest(SoledadTestBase):

    @defer.inlineCallbacks
    def test_message_collection(self):
        # given
        mbx = yield self.account.getMailbox('INBOX')
        input_mail = MailBuilder().build_input_mail()

        # when
        yield MailboxIndexerListener.listen(self.account, 'INBOX', self.mail_store, self.search_engine)
        yield mbx.addMessage(input_mail.raw, [], notify_just_mdoc=False)

        # then
        yield self.wait_in_reactor()  # event handlers are called async, wait for it

        mails, mail_count = self.search_engine.search('in:all')
        self.assertEqual(1, mail_count)
        self.assertEqual(1, len(mails))

    def wait_in_reactor(self):
        d = defer.Deferred()

        def done_waiting():
            d.callback(None)

        reactor.callLater(1, done_waiting)
        return d
