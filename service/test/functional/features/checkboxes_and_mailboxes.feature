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

Feature: Checkboxes
  As a user of Pixelated
  I want to use checkboxes to manage my emails
  So I can manage more than one email at once

  Scenario: User has a list of emails in each mailboxes that needs to be managed
    Given I have a mail in my inbox
    When I mark the first unread email as read
      And I delete the email
    When I select the tag 'trash'
    Then the deleted mail is there
    When I check all emails
      And I delete them permanently
    Then I should not see any email

