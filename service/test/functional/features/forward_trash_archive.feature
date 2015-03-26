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

Feature: forward and deletion
  As a user of Pixelated
  I want to forward emails using CC and Bcc features
  So I can take actions

  Scenario: User forwards a mail, add CC and BCC address, later trash the mail
    Given I have a mail in my inbox
    When I open the first mail in the 'inbox'
      And I choose to forward this mail
    When for the 'CC' field I enter 'pixelated@friends.org'
      And for the 'Bcc' field I enter 'pixelated@family.org'
      And I forward this mail
    When I open the first mail in the 'sent'
    Then I see the mail has a cc and a bcc recipient
    When I choose to trash
#    Then I see that mail under the 'trash' tag
    When I select the tag 'trash'
      And I open the first mail in the mail list