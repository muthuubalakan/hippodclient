import os
import tempfile
import shutil
import textwrap

from unittest import TestCase

import hippodclient



URL = "http://127.0.0.1/"
TIMEOUT = 10


def gen_rand_image_path():
    tmpdir = tempfile.mkdtemp()

    cwd = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(cwd, "graph.png")
    if not os.path.isfile(img_path):
        return None
    return img_path

def file_log_path():
    cwd = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(cwd, "hippod.log")
    if not os.path.isfile(img_path):
        return None
    return img_path

def file_py_path():
    return os.path.abspath(__file__)

def gen_snippet_file(offset):
    tmpdir = tempfile.mkdtemp()
    tmpfile = os.path.join(tmpdir, "snippet.py")
    content = """
    import sys
    import matplotlib
    # Force matplotlib to not use any Xwindows backend.
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np
    t = np.arange(0.0, 2.0, 0.01)
    s = {} + np.sin(2*np.pi*t)
    plt.plot(t, s)

    plt.xlabel('time (s)')
    plt.ylabel('voltage (mV)')
    plt.title('About as simple as it gets, folks')
    plt.grid(True)
    plt.savefig(sys.argv[1])
    """.format(offset)
    fd = open(tmpfile, "w")
    fd.write(textwrap.dedent(content))
    fd.close()
    return tmpdir, tmpfile


class TestHippodClient(TestCase):

    def test_is_initiable(self):
        hippodclient.Test()
        hippodclient.Container(timeout=TIMEOUT)

    def test_upload(self):
        c = hippodclient.Container(timeout=TIMEOUT)
        c.set_url(URL)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("random title")
        t.categories_set("team:bar")
        t.attachment.tags_add("foo", "bar")
        t.achievement.result = "passed"

        c.add(t)
        c.sync()

    def test_minimal_passed(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("random title for minimal example, passed")
        t.categories_set("team:bp")
        t.achievement.result = "passed"

        c.add(t)
        c.upload()

    def test_minimal_failed(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("random title for minimal example, failed")
        t.categories_set("team:foo")
        t.achievement.result = "failed"

        c.add(t)
        c.upload()

    def test_minimal_nonapplicable(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("random title for minimal example, nonapplicable")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        c.add(t)
        c.upload()

    def test_minimal_tags_category(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Minimal Test with Categories and Tags")
        t.categories_set("team:foo", "bar", "foo", "trump")
        t.attachment.tags_set("bar", "foo", "trump", "obama", "merkel", "holande")
        t.attachment.references_set("ref:1", "ref:2", "ref:3", "ref:4")
        t.achievement.result = "passed"

        c.add(t)
        c.upload()

    def test_markdown_minimal(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Markdown Test")
        description = """
        # This is a first level heading

        ## Second Level Heading

        ### Third level heading

        """
        t.description_markdown_set(description)
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        c.add(t)
        c.upload()


    def test_snippet_item(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Snippet Test Item")
        t.description_plain_set("Simple Description")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        tmp_dir, graph_path = gen_snippet_file(1)
        t.snippet_file_add(graph_path, "x-snippet-python3-matplot-png")

        c.add(t)
        c.upload()
        shutil.rmtree(tmp_dir)

    def test_snippet_multiple_item(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Snippet Test Item Multiple")
        t.description_plain_set("Simple Description")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        tmps = []
        for i in range(10):
            tmp_dir, graph_path = gen_snippet_file(i)
            t.snippet_file_add(graph_path, "x-snippet-python3-matplot-png")
            tmps.append(tmp_dir)

        c.add(t)
        c.upload()
        for tmp_dir in tmps:
            shutil.rmtree(tmp_dir)


    def test_snippet_achievement(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Snippet Test Achievement")
        t.description_plain_set("simple description")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        tmp_dir, graph_path = gen_snippet_file(1)
        t.achievement.snippet_file_add(graph_path, "x-snippet-python3-matplot-png")

        c.add(t)
        c.upload()
        shutil.rmtree(tmp_dir)


    def test_snippet_multiple_achievement(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Snippet Test Achievement Multiple")
        t.description_plain_set("Simple Description")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"

        tmps = []
        for i in range(10):
            tmp_dir, graph_path = gen_snippet_file(i)
            t.achievement.snippet_file_add(graph_path, "x-snippet-python3-matplot-png")
            tmps.append(tmp_dir)

        c.add(t)
        c.upload()
        for tmp_dir in tmps:
            shutil.rmtree(tmp_dir)


    def test_mass_upload(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Mass Upload")
        t.description_plain_set("Simple Description")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"
        c.add(t)
        for i in range(10):
            c.upload()


    def test_different_achievements(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Different Tests")
        t.categories_set("team:foo")
        t.achievement.result = "passed"
        c.add(t)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Different Achievements")
        t.categories_set("team:foo")
        t.achievement.result = "failed"
        c.add(t)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Different Achievements")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"
        c.add(t)

        c.upload()

    def test_image_item(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Image Item")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"
        image = gen_rand_image_path()
        self.assertTrue(image)
        t.data_file_add(image)
        c.add(t)
        c.upload()

    def test_image_achievement(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Image Achievement")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"
        image = gen_rand_image_path()
        self.assertTrue(image)
        t.achievement.data_file_add(image)
        c.add(t)
        c.upload()

    def test_multiple_data_achievement(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Multiple Data Achievements")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"
        path = gen_rand_image_path()
        self.assertTrue(path)
        t.achievement.data_file_add(path)
        path = file_py_path()
        self.assertTrue(path)
        t.achievement.data_file_add(path)
        c.add(t)
        c.upload()

    def test_multiple_data_items(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Multiple Data Items")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"
        # add image
        path = gen_rand_image_path()
        self.assertTrue(path)
        t.data_file_add(path)
        # add python file
        path = file_py_path()
        self.assertTrue(path)
        t.data_file_add(path)
        # add log file
        path = file_log_path()
        self.assertTrue(path)
        t.data_file_add(path)
        c.add(t)
        c.upload()

    def test_multiple_data_items_achievements(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Multiple Data Items and Achievements")
        t.categories_set("team:foo")
        t.achievement.result = "nonapplicable"
        # add image
        path = gen_rand_image_path()
        self.assertTrue(path)
        t.data_file_add(path)
        # add python file
        path = file_py_path()
        self.assertTrue(path)
        t.data_file_add(path)
        # add log file
        path = file_log_path()
        self.assertTrue(path)
        t.data_file_add(path)
        # add image
        path = gen_rand_image_path()
        self.assertTrue(path)
        t.achievement.data_file_add(path)
        # add python file
        path = file_py_path()
        self.assertTrue(path)
        t.achievement.data_file_add(path)
        # add log file
        path = file_log_path()
        self.assertTrue(path)
        t.achievement.data_file_add(path)

        c.add(t)
        c.upload()
