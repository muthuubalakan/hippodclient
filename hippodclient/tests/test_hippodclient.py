from unittest import TestCase

import hippodclient

class TestHippodClient(TestCase):

    def test_is_initiable(self):
        hippodclient.Test()
        hippodclient.Core()
