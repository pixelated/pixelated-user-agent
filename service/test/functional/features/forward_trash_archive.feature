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

Feature: forward_trash_archive

  Scenario: User forwards a mail, add CC and BCC address, later trash the mail
    Given I have a mail in my inbox
    When I open the first mail in the 'inbox'
    Then I choose to forward this mail
    # And for the 'CC' field I type 'ab' and chose the first contact that shows
    # And for the 'Bcc' field I type 'fr' and chose the first contact that shows
    Given for the 'CC' field I enter 'pixelated@friends.org'
    And for the 'Bcc' field I enter 'pixelated@family.org'
    Then I forward this mail
    When I open the first mail in the 'sent'
    Then I see the mail has a cc and a bcc recipient
    And I choose to trash
    Then I see that mail under the 'trash' tag
