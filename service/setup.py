#!/usr/bin/env python

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
      packages=['pixelated'],
      install_requires=[
          'scrypt',
          'Twisted==12.2.0',
          'flask==0.10.1',
          'scanner==0.0.5',
          'requests==2.3.0',
          'pytest==2.6.0',
          'mock==1.0.1',
          'httmock==1.2.2',
          'srp==1.0.4',
          'dirspec==13.10',
          'u1db==13.09',
          'leap.keymanager==0.3.8',
          'leap.soledad.common==0.5.2',
          'leap.soledad.client==0.5.2',
          'leap.mail==0.3.9-1-gc1f9c92',
      ],
     )
