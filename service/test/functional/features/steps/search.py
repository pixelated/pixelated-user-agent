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
from time import sleep

from selenium.webdriver.common.keys import Keys
from common import *
from hamcrest import *


@when('I search for a mail with the words "{search_term}"')
def impl(context, search_term):
    search_field = find_element_by_css_selector(context, '#search-trigger input[type="search"]')
    search_field.send_keys(search_term)
    search_field.send_keys(Keys.ENTER)
    sleep(1)


@then('I see one or more mails in the search results')
def impl(context):
    lis = find_elements_by_css_selector(context, '#mail-list li')
    assert_that(len(lis), greater_than_or_equal_to(1))
