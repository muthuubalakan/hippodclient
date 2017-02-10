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
        t.categories_set("team:bar")
        t.attachment.tags_add("foo", "bar")
        t.achievement.result = "passed"

        c.add(t)
        c.sync()

    def test_minimal_passed(self):
        c = hippodclient.Container(url="http://127.0.0.1/")

        t = hippodclient.Test()
        t.title_set("random title for minimal example, passed")
        t.categories_set("team:foo")
        t.achievement.result = "passed"

        c.add(t)
        c.upload()

    def test_minimal_failed(self):
        c = hippodclient.Container(url="http://127.0.0.1/")

        t = hippodclient.Test()
        t.title_set("random title for minimal example, failed")
        t.categories_set("team:foo")
        t.achievement.result = "failed"

        c.add(t)
        c.upload()

    def test_minimal_nonapplicable(self):
        c = hippodclient.Container(url="http://127.0.0.1/")

        t = hippodclient.Test()
        t.title_set("random title for minimal example, nonapplicable")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        c.add(t)
        c.upload()
