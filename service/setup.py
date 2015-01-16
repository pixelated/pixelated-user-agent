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

# next line is a fix to this error that occurs with nose > 1.1.2 and the debian
# python: http://bugs.python.org/issue15881#msg170215
import multiprocessing

import setuptools
from setuptools import setup
from collections import defaultdict
import os


def _folder_for(file):
    broken_path = file.split('/')
    new_path = "web-ui/app/" + "/".join(broken_path[3:(len(broken_path) - 1)])
    return new_path[0:-1] if new_path[-1] == '/' else new_path


def _create_data_files(original_files):
    data_files_hash = defaultdict(list)

    for file in original_files:
        data_files_hash[_folder_for(file)].append(file)

    return data_files_hash.items()


def _web_ui_files():
    web_ui_files = []
    for root, dirname, filenames in os.walk('../web-ui/dist'):
        for filename in filenames:
            web_ui_files.append(os.path.join(root, filename))
    return web_ui_files


def data_files():
    certificates = ('pixelated/certificates', ['pixelated/certificates/example.wazokazi.is.ca.crt'])

    _data_files = _create_data_files(_web_ui_files())
    _data_files.append(certificates)

    return _data_files


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='pixelated-user-agent',
      version='0.1',
      description='API to serve the pixelated front-end requests',
      long_description=read('README.md'),
      author='Thoughtworks',
      author_email='pixelated-team@thoughtworks.com',
      url='http://pixelated-project.github.io',
      packages=[
          'pixelated',
          'pixelated.adapter',
          'pixelated.adapter.listeners',
          'pixelated.adapter.model',
          'pixelated.adapter.search',
          'pixelated.adapter.services',
          'pixelated.adapter.soledad',
          'pixelated.bitmask_libraries',
          'pixelated.config',
          'pixelated.certificates',
          'pixelated.support',
          'pixelated.controllers'
      ],
      test_suite='nose.collector',
      install_requires=[
           'pyasn1==0.1.7',
           'gnupg==1.4.0',
           'Twisted==14.0.2',
           'klein==0.2.3',
           'requests==2.5.0',
           'srp==1.0.5',
           'dirspec==13.10',
           'u1db==13.09',
           'leap.keymanager==0.3.8',
           'leap.soledad.common==0.6.3',
           'leap.soledad.client==0.6.3',
           'leap.mail==0.3.9-1-gc1f9c92',
           'whoosh==2.6.0'
      ],
      entry_points={
          'console_scripts': [
              'pixelated-user-agent = pixelated.runserver:setup'
          ]
      },
      data_files=data_files(),
      include_package_data=True
)
