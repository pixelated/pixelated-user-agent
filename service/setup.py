#!/usr/bin/env python
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

import sys
if 'develop' in sys.argv:
    sys.argv.append('--always-unzip')

from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='Pixelated User Agent Service',
      version='0.1',
      description='API to serve the pixelated front-end requests',
      long_description=read('README.md'),
      author='Thoughtworks',
      author_email='pixelated-team@thoughtworks.com',
      url='http://pixelated-project.github.io',
      packages=['pixelated', 'pixelated.adapter', 'pixelated.bitmask_libraries', 'pixelated.config', 'pixelated.certificates'],
      test_suite='nose.collector',
      install_requires=[
          'Twisted',
          'flask',
          'scanner',
          'requests',
          'srp==1.0.4',
          'dirspec==13.10',
          'u1db==13.09',
          'leap.keymanager==0.3.8',
          'leap.soledad.common==0.5.2',
          'leap.soledad.client==0.5.2',
          'leap.mail==0.3.9-1-gc1f9c92',
          'nose',
          'mock',
          'httmock',
          'gunicorn'
      ],
      entry_points={
        'console_scripts': [
            'pixelated-user-agent = pixelated.user_agent:setup'
        ]
      }
     )
