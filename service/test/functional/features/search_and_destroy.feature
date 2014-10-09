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

Feature: search html mail and destroy

  @wip
  Scenario: User searches for a mail and deletes it
    When I search for a mail with the words "this is a html mail"
    When I open the first mail in the mail list
    Then I see one or more mails in the search results
    Then I see if the mail has html content
    When I try to delete the first mail
    # Then I learn that the mail was deleted
    When I select the tag 'trash'
    Then the deleted mail is there
