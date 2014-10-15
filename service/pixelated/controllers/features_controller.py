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

from pixelated.controllers import respond_json
import os


class FeaturesController:
    DISABLED_FEATURES = ['draftReply', 'signatureStatus', 'encryptionStatus', 'contacts']

    def __init__(self):
        pass

    def features(self):
        try:
            disabled_features = {'logout': os.environ['DISPATCHER_LOGOUT_URL']}
        except KeyError:
            disabled_features = {}
        return respond_json({'disabled_features': self.DISABLED_FEATURES, 'dispatcher_features': disabled_features})