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

Feature: compose mail, save draft and send mail
  As a user of Pixelated
  I want to save drafts
  So I can review and send them later

  Scenario: user composes and email, save the draft, later sends the draft and checks the sent message
    When I compose a message with
      | subject          | body                                        |
      | Pixelated rocks! | You should definitely use it. Cheers, User. |
      And for the 'To' field I enter 'pixelated@friends.org'
      And I save the draft
    When I select the tag 'drafts'
    When I open the first mail in the mail list
     And I send it
    When I select the tag 'sent'
      And I open the first mail in the mail list
    Then I see that the subject reads 'Pixelated rocks!'
    Then I see that the body reads 'You should definitely use it. Cheers, User.'
