from unittest import TestCase

import hippodclient

class TestHippodClient(TestCase):

    def test_is_initiable(self):
        hippodclient.Test()
        hippodclient.Container()

    def test_upload(self):
        c = hippodclient.Container()
        c.set_url("http://127.0.0.1/")

        t = hippodclient.Test()
        t.title_set("random title")
        t.categories_set("team:cp")
        t.attachment.tags_add("foo", "bar")
        t.achievement.result = "passed"

        c.add(t)
        r = c.sync()
        print(r)

