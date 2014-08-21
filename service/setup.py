#!/usr/bin/env python

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
      packages=['pixelated', 'pixelated.adapter', 'pixelated.bitmask_libraries'],
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
      package_data={'': ['config/*']},
      entry_points={
        'console_scripts': [
            'pixelated-user-agent = pixelated.user_agent:setup'
        ]
      }
     )
