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

from mock import MagicMock
from twisted.trial import unittest
from pixelated.resources import BaseResource


class TestBaseResource(unittest.TestCase):
    def test_get_soledad_service(self):
        mock_services_factory = MagicMock()
        base_resource = BaseResource(mock_services_factory)

        self.assertEqual(base_resource.soledad('request'), mock_services_factory.services()._leap_session.soledad)
