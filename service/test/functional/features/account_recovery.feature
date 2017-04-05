#
# Copyright (c) 2017 ThoughtWorks, Inc.
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

@smoke
Feature: Account Recovery
  As a user of Pixelated
  I want to recover my account
  So that I can see my emails if I lose my password

  Scenario: Sending recovery code
    Given I am logged in Pixelated
    When I go to the backup account page
    And I submit my backup account
    Then I see the confirmation of this submission
    And I logout from the header
    And I should see the login page

  Scenario: Recovering an account
    Given I am on the account recovery page
    When I submit admin recovery code
    And I submit user recovery code
    And I submit new password
    Then I see the backup account step
