from unittest import TestCase

import hippodclient

class TestJoke(TestCase):

    def test_is_string(self):
        s = hippodclient.Test()
        self.assertTrue(isinstance(s, hippodclient.Test()))
