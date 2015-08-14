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

Feature: Attachments
  As a user of Pixelated
  I want to download attachments of mails I received
  So that my peers are able to send me any kind of content, not just text

  Scenario: User opens a mail attachment
    Given I have a mail with an attachment in my inbox
    When I open the first mail in the 'inbox'
    Then I see the mail has an attachment
    #When I open click on the first attachment
    #Then the browser downloaded a file
