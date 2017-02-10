from unittest import TestCase

import hippodclient

class TestHippodClient(TestCase):

    def test_is_initiable(self):
        hippodclient.Test()
        hippodclient.Container()

    def test_upload(self):
        c = hippodclient.Container()
        c.set_url("http://localhost")

        t = hippodclient.Test()
        t.title_set("random title")

        t.categories_set("team:cp")

        t.attachment.responsible = ""
        t.attachment.tags_add("foo")
        t.attachment.tags_add("foo", "bar")
        t.attachment._tags_cleanup()

        t.achievement.result = ""
        c.add(t)

        c.sync()

