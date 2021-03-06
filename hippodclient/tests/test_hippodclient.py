import os
import tempfile
import shutil
import textwrap
import string
import random

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

def random_category():
    category_first = ["team:foo", "team:bar", "team:qux"]
    category_second  = ["os-core", "configuration", "routing", "init", "networking"]
    category_second += ["logging", "bootloader", "se-linux" ]
    category = []
    category.append(random.choice(category_first))
    for i in range(random.randint(1, 3)):
        category.append(random.choice(category_second))
    return category

def random_tags():
    tags  = ["performance", "security", "shell", "daemon", "compiler", "runtime"]
    tags += ["kernel", "userspace", "realtime", "irq", "softirq", "thread"]
    ret = []
    for i in range(random.randint(1, 10)):
        ret.append(random.choice(tags))
    return ret

def random_result():
    results = ["passed", "exception", "failed", "nonapplicable" ]
    return random.choice(results)

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


    def test_minimal_passed(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Minimal Test with Passed Result")
        t.categories_set(*random_category())
        t.achievement.result = "passed"

        c.add(t)
        c.upload()

    def test_minimal_failed(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Minimal Test with Failed Result")
        t.categories_set(*random_category())
        t.achievement.result = "failed"

        c.add(t)
        c.upload()

    def test_minimal_exception(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Minimal Test with Exception Result")
        t.categories_set(*random_category())
        t.achievement.result = "exception"

        c.add(t)
        c.upload()

    def test_minimal_nonapplicable(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Minimal Test with Non Applicable Result")
        t.categories_set(*random_category())
        t.achievement.result = "nonapplicable"

        c.add(t)
        c.upload()

    def test_minimal_tags_category(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Minimal Test with Categories and Tags")
        t.categories_set(*random_category())
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
        t.categories_set(*random_category())
        t.achievement.result = "nonapplicable"

        c.add(t)
        c.upload()


    def test_snippet_item(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Snippet Test Item")
        t.description_plain_set("Simple Description")
        t.categories_set(*random_category())
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
        t.categories_set(*random_category())
        t.achievement.result = "nonapplicable"

        tmps = []
        for i in range(4):
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
        t.categories_set(*random_category())
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
        t.categories_set(*random_category())
        t.achievement.result = "nonapplicable"

        tmps = []
        for i in range(4):
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
        t.categories_set(*random_category())
        t.achievement.result = "nonapplicable"
        c.add(t)
        for i in range(10):
            c.upload()


    def test_different_achievements(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Different Tests")
        t.categories_set(*random_category())
        t.achievement.result = "passed"
        c.add(t)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Different Achievements")
        t.categories_set(*random_category())
        t.achievement.result = "failed"
        c.add(t)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Different Achievements")
        t.categories_set(*random_category())
        t.achievement.result = "nonapplicable"
        c.add(t)

        c.upload()

    def test_image_item(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)
        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Image Item")
        t.categories_set(*random_category())
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
        t.categories_set(*random_category())
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
        t.categories_set(*random_category())
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
        t.categories_set(*random_category())
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
        t.categories_set(*random_category())
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

    def test_category_arg_tuple(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Test with Categories as Array")
        t.categories_set(random_category())
        t.achievement.result = random_result()

        c.add(t)
        c.upload()

    def test_category_arg_list(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Test with Categories as Argument List")
        t.categories_set(*random_category())
        t.achievement.result = random_result()

        c.add(t)
        c.upload()

    def test_category_arg_string(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Test with Categories as String")
        t.categories_set("foo")
        t.achievement.result = random_result()

        c.add(t)
        c.upload()

    def test_tags_arg_tuple_set(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Test with Tags as Array via Set")
        t.categories_set(*random_category())
        t.attachment.tags_set(random_tags())
        t.achievement.result = random_result()

        c.add(t)
        c.upload()

    def test_tags_arg_list_set(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Test with Tags as Argument List via Set")
        t.categories_set(*random_category())
        t.attachment.tags_set(*random_tags())
        t.achievement.result = random_result()

        c.add(t)
        c.upload()

    def test_tags_arg_tuple_add(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Test with Tags as Array via Add")
        t.categories_set(*random_category())
        t.attachment.tags_add(random_tags())
        t.attachment.tags_add(random_tags())
        t.attachment.tags_add(random_tags())
        t.achievement.result = random_result()

        c.add(t)
        c.upload()

    def test_tags_arg_list_add(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Test with Tags as Argument List via Add")
        t.categories_set(*random_category())
        t.attachment.tags_add(*random_tags())
        t.attachment.tags_add(*random_tags())
        t.attachment.tags_add(*random_tags())
        t.achievement.result = random_result()

        c.add(t)
        c.upload()

    def test_responsible(self):
        c = hippodclient.Container(url=URL, timeout=TIMEOUT)

        t = hippodclient.Test()
        t.submitter_set("anonymous")
        t.title_set("Responsible Set Test")
        t.categories_set(*random_category())
        t.attachment.responsible_set("anonymous")
        t.achievement.result = random_result()

        c.add(t)
        c.upload()


    def mass(self):
        for i in range(5000):
            c = hippodclient.Container(url=URL, timeout=TIMEOUT)
            title = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(1))

            t = hippodclient.Test()
            t.submitter_set("anonymous")
            t.title_set(title)
            t.categories_set(*random_category())
            t.achievement.result = random_result()

            c.add(t)
            c.upload()
