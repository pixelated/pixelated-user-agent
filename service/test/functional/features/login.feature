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

Feature: login and logout
  As a user of Pixelated
  I want to log in to my account
  So I can see my emails

  Scenario: Existing user logs into his account
    Given Account for user username exists
    And I have a mail for username in my inbox
    When I open the login page
    And I enter username and password as credentials
    And I click on the login button
    Then I have mails
