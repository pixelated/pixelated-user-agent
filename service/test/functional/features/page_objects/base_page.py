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

from steps.common import (
    fill_by_css_selector,
    find_element_by_css_selector)


class BasePage(object):
    def __init__(self, context, base_url):
        self.context = context
        self.timeout = 30
        self.base_url = base_url

    def find_element_by_css_selector(self, loc):
        return find_element_by_css_selector(self.context, loc)

    def fill_by_css_selector(self, loc, text):
        fill_by_css_selector(self.context, loc, text)

    def visit(self):
        self.context.browser.get(self.base_url)
