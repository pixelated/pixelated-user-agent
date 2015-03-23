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
from common import *


def click_first_element_with_class(context, classname):
    elements = context.browser.find_elements_by_class_name(classname)
    elements[0].click()


def is_side_nax_expanded(context):
    e = context.browser.find_elements_by_class_name('content')[0].get_attribute('class').count(u'move-right') == 1
    return e


def expand_side_nav(context):
    if is_side_nax_expanded(context):
        return

    toggle = context.browser.find_elements_by_class_name('side-nav-toggle')[0]
    toggle.click()


@when('I select the tag \'{tag}\'')
def impl(context, tag):
    wait_for_user_alert_to_disapear(context)
    expand_side_nav(context)

    wait_until_element_is_visible_by_locator(context, (By.ID, 'tag-%s' % tag), 20)

    e = find_element_by_id(context, 'tag-%s' % tag.lower())
    e.click()


@when('I am in  \'{tag}\'')
def impl(context, tag):
    expand_side_nav(context)

    wait_until_element_is_visible_by_locator(context, (By.ID, 'tag-%s' % tag), 20)
    e = find_element_by_id(context, 'tag-%s' % tag)
    assert "selected" in e.get_attribute("class")
