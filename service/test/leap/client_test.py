import sys
import os
sys.path.insert(0, os.environ['APP_ROOT'])

from app.leap.client import Client


def test_initialization():
    client = Client()
    print('Run')
