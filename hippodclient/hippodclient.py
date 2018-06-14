# -*- coding: utf-8 -*-

import json
import pprint
import base64
import re
import os
import sys
import datetime
import mimetypes
import getpass
import textwrap
import asyncio
import aiohttp


REQUEST_TIMEOUT = 5


# custom exceptions
class ArgumentException(Exception): pass
class ConfigurationException(Exception): pass
class InternalException(Exception): pass
class TransformException(Exception): pass

PASSED = "passed"
FAILED = "failed"
NONAPPLICABLE = "nonapplicable"
EXCEPTION = "exception"

DEFAULT_RESULT = NONAPPLICABLE
DEFAULT_USERNAME = "anonymous"


def create_file_entry(file_name, mime_type):
        """ Create file entry for object-item data or achievement. """
        # Check first if the file is available
        if not os.path.isfile(file_name):
            emsg = "File '{}' is not available".format(file_name)
            raise ArgumentException(emsg)

        if not mime_type:
            mime_type, _ = mimetypes.guess_type(file_name)
            if mime_type is None:
                mime_type = TestMimeTypes.guess_type(file_name)

        with open(file_name, "rb") as f:
            file_content = base64.b64encode(f.read())

        # Create entry for object item data
        entry = dict()
        entry["name"] = os.path.basename(file_name)
        entry["mime-type"] = mime_type
        entry["data"] = file_content.decode()
        return entry

def create_snippet_entry(file_name, mime_type, name):
        if not os.path.isfile(file_name):
            emsg = "File '{}' is not available".format(file_name)
            raise ArgumentException(emsg)
        if mime_type != "x-snippet-python3-matplot-png":
            emsg = "Snippet only support for x-snippet-python3-matplot-png" \
                   " - for now. Not: {}".format(mime_type)
            raise ArgumentException(emsg)

        with open(file_name, "rb") as f:
            file_content = base64.b64encode(f.read())

        entry = dict()
        entry["mime-type"] = mime_type
        entry["data"] = file_content.decode()
        if name:
            entry["name"] = name

        return entry

def has_invalid_character(string):
    return not bool(re.match("^[a-z0-9-:]*$", string))

def to_list(args):
    # depending how the user calls a function we want a identical
    # behavior: func(a, b, c, d) and func([a, b, c, d])
    if len(args) == 1 and type(args[0]) is list:
        return list(args[0])
    return list(args)

class TestMimeTypes():
    types_map = dict()
    types_map[".pcap"] = 'application/vnd.tcpdump.pcap'


    @staticmethod
    def guess_type(file_name):
        _ , ext = os.path.splitext(os.path.basename(file_name))

        if ext in TestMimeTypes.types_map:
            return TestMimeTypes.types_map[ext]
        else:
            return "binary/octet-stream"


class Container(object):

    # Supported HTTP methods
    HTTP_GET  = "GET"
    HTTP_POST = "POST"

    # URL path
    URL_API_OBJECTS = "api/v1/object"

    def __init__(self, url=None, timeout=REQUEST_TIMEOUT):
        self._init_defaults()
        self.timeout = timeout
        self.url = url
        self.loop = asyncio.get_event_loop()

    def _init_defaults(self):
        self.tests = list()

    def set_url(self, url):
        self.url = url

    def add(self, test):
        self.tests.append(test)

    def _check_pre_sync(self):
        if not self.url:
            raise ConfigurationException("no hippod server URL specified")

    async def _send_data(self, data):
        self.user_agent_headers = {'Content-type': 'application/json',
                                   'Accept': 'application/json',
                                   'User-Agent' : 'Hippodclient/1.0+'
                                   }
        seperator = "/"
        if self.url.endswith("/"): seperator = ""
        full_url = "{}{}{}".format(self.url, seperator, "api/v1/object")
        data = str.encode(data)
        async with aiohttp.ClientSession() as session:
            async with session.post(full_url, data=data) as resp:
                print("Response: {}".format(resp.status))
        return (True, None)

    def sync(self):
        self._check_pre_sync()
        ret_list = list()
        for test in self.tests:
            json_data = test.json()
            ret = self.loop.run_until_complete(self._send_data(json_data))
            ret_list.append(ret)
        return ret_list
    # just an alias for sync


class Test(object):

    class Attachment(object):

        def __init__(self):
            self.tags = list()
            self.references = list()
            self.responsible = DEFAULT_USERNAME

        def responsible_set(self, name):
            self.responsible = name

        def tags_set(self, *tags):
            self.tags = list()
            tags = to_list(tags)
            for tag in tags:
                if has_invalid_character(tag):
                    emsg = "tag contain invalid char which is not allowed ([a-z0-9-:]): {}"
                    emsg.format(tag)
                    raise ArgumentException(emsg)
                self.tags.append(tag)
            self._tags_cleanup()

        def tags_add(self, *tags):
            tags = to_list(tags)
            for tag in tags:
                if has_invalid_character(tag):
                    emsg = "tag contain invalid char which is not allowed ([a-z0-9-:]): {}"
                    emsg.format(tag)
                    raise ArgumentException(emsg)
                self.tags.append(tag)
            self._tags_cleanup()

        def _tags_cleanup(self):
            # remove duplicate tags in list
            seen = set()
            self.tags = [x for x in self.tags if x not in seen and not seen.add(x)]

        def references_set(self, *references):
            self.references = []
            references = to_list(references)
            for reference in references:
                self.references.append(reference)
            self._references_cleanup()

        def references_add(self, *references):
            references = to_list(references)
            for reference in references:
                self.references.append(reference)
            self._references_cleanup()

        def _references_cleanup(self):
            # remove duplicate references in list
            seen = set()
            self.references = [x for x in self.references if x not in seen and not seen.add(x)]

        def transform(self):
            d = dict()
            if len(self.tags) > 0:
                d["tags"] = self.tags
            if len(self.references) > 0:
                d["references"] = self.references
            d["responsible"] = self.responsible
            return d



    class Achievement(object):

        def __init__(self):
            self.result = DEFAULT_RESULT
            self.test_date = datetime.datetime.now().isoformat('T')
            print("The date is ", self.test_date)
            self.data = list()
            self.anchor = None

        def result_set(self, result, date=None):
            if result not in (PASSED, FAILED, NONAPPLICABLE, EXCEPTION):
                emsg = "only passed, failed and nonapplicable supported"
                raise ArgumentException(emsg)
            if date is None:
                date = datetime.datetime.now().isoformat('T')
            self.result = result
            self.test_date = date

        def anchor_set(self, anchor):
            if type(anchor) is not str:
                raise ArgumentException("anchor must be an string, not {}".format(type(anchor)))
            self.anchor = anchor

        def data_file_add(self, filepath, mime_type=None):
            entry = create_file_entry(filepath, mime_type)
            self.data.append(entry)

        def snippet_file_add(self, filepath, type, name=None):
            entry = create_snippet_entry(filepath, type, name)
            self.data.append(entry)

        def transform(self):
            root = dict()
            root["result"] = self.result
            root["test-date"] = self.test_date
            if len(self.data) > 0:
                root["data"] = self.data
            if self.anchor:
                root["anchor"] = self.anchor
            return root






    def init_defaults(self):
        self.submitter = getpass.getuser()
        self.title = None
        self.categories = list()
        self.data = list()

    def __init__(self, debug=False):
        self.debug = debug
        self.init_defaults()
        self.attachment = Test.Attachment()
        self.achievement = Test.Achievement()

    def submitter_set(self, submitter):
        val_type = type(submitter)
        if val_type is not str:
            raise ArgumentException("submitter must be an string, not {}".format(val_type))
        self.submitter = submitter

    def description_set(self, description, type="plain", detent=False):
        if (type == "markdown"):
            mime_type = "text/markdown"
        else:
            mime_type = "text/plain"

        if detent == True:
            description = textwrap.dedent(description)

        # iterate over data structure and if a description
        # is alread there: remove and overwrite
        for i in range(len(self.data)):
            if self.data[i]["type"] == "description":
                del self.data[i]
                break
        data_item = dict()
        data_item["type"] = "description"
        data_item["mime-type"] = mime_type
        data_item["data"] = (base64.b64encode(description.encode())).decode()
        self.data.append(data_item)

    def description_markdown_set(self, description):
        self.description_set(description, type="markdown", detent=True)

    def description_plain_set(self, description):
        self.description_set(description)

    def title_set(self, title):
        self.title = title

    def data_file_add(self, filepath, mime_type=None):
        entry = create_file_entry(filepath, mime_type)
        self.data.append(entry)

    def snippet_file_add(self, filepath, type, name=None):
        entry = create_snippet_entry(filepath, type, name)
        self.data.append(entry)

    def categories_set(self, *categories):
        self.categories = list()
        categories = to_list(categories)
        for category in categories:
            if has_invalid_character(category):
                emsg = "category contains invalid char which is not allowed(): {}"
                emsg.format(category)
                raise ArgumentException(emsg)
            self.categories.append(category)

    def transform(self):
        d = dict()
        if not self.title:
            emsg = "test case inpure, title missing"
            raise TransformException(emsg)
        d['title'] = self.title
        if not self.categories or len(self.categories) == 0:
            emsg = "categories missing, need at least one level of category"
            raise TransformException(emsg)
        d["categories"] = self.categories
        d["version"] = 0
        if len(self.data) > 0:
            d["data"] = self.data
        return d

    def json(self):
        root = dict()
        root["submitter"] = self.submitter
        root["achievements"] = list()
        root["achievements"].append(self.achievement.transform())

        root["attachment"] = self.attachment.transform()

        root["object-item"] = self.transform()
        pprint.pprint(root)
        return json.dumps(root, sort_keys=True, separators=(',', ': '))


if __name__ == "__main__":
    sys.stderr.write("Python client library to interact with HippoD\n")
    sys.stderr.write("Please import this file and use provided function\n")
