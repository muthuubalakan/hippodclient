# -*- coding: utf-8 -*-

import json
import pprint
import base64
import re
import os
import sys
import time
import mimetypes
import getpass

try:
    # python3
    import urllib.request as urllib_request
except ImportError:
    # python2
    import urllib2 as urllib_request

REQUEST_TIMEOUT = 3


# custom exceptions
class ArgumentException(Exception): pass
class ConfigurationException(Exception): pass
class InternalException(Exception): pass

PASSED = "passed"
FAILED = "failed"
NONAPPLICABLE = "nonapplicable"

DEFAULT_RESULT = NONAPPLICABLE
DEFAULT_USERNAME = "anomymous"


def create_file_entry(self, file_name, mime_type = None):
        """ Create file entry for object-item data or achievement. """
        # Check first if the file is available
        if not os.path.isfile(file_name):
            raise Exception("File '{}' is not available and "
                            "can't be sent to the HippoD server.".format(file_name))

        if not mime_type:
            # Get mime type for file
            mime_type, _ = mimetypes.guess_type(file_name)
            if mime_type is None:
                # Search for the mime type in the addition test mime types
                mime_type = TestMimeTypes.guess_type(file_name)

        # Convert file content to base64
        with open(file_name, "rb") as f:
            file_content = self.encode_base64_data(f.read())

        # Create entry for object item data
        file_entry = {"name" :      os.path.basename(file_name),
                      "mime-type" : mime_type,
                      "data" :      str(file_content)
                     }
        return file_entry

def create_snippet_entry(self, file_name, type_, name):
        if not os.path.isfile(file_name):
            raise Exception("Snippet file '{}' is not available and "
                            "can't be sent to the HippoD server.".format(file_name))
        if type_ != "x-snippet-python3-mathplot-png":
            raise Exception("Snippet only support for x-snippet-python3-mathplot-png"
                            " - for now. Not: {}".format(type_))

        # Convert file content to base64
        with open(file_name, "rb") as f:
            file_content = self.encode_base64_data(f.read())

        # Create entry for object item data
        file_entry = {
                      "mime-type" : type_,
                      "data" :      str(file_content)
                     }
        if name:
            file_entry["name"] = name
        return file_entry


class TestMimeTypes():

    # Additional mime types which are not available
    # in the standard mime types python libary
    types_map = {
                 '.pcap' : 'application/vnd.tcpdump.pcap',
                }

    @staticmethod
    def guess_type(file_name):
        _ , ext = os.path.splitext(os.path.basename(file_name))

        if ext in TestMimeTypes.types_map:
            return TestMimeTypes.types_map[ext]
        else:
            return "binary/octet-stream"


class Core(object):

    # Supported HTTP methods
    HTTP_GET  = "GET"
    HTTP_POST = "POST" 

    # URL path
    URL_API_OBJECTS = "api/v1/object"
    URL_API_USERS   = "api/v1/users"

    def __init__(self):
        self.init_defaults()


    def init_defaults(self):
        self.tests = list()
        self.url = None

    def set_url(self, url):
        self.url = url

    def add(self, test):
        self.tests.append(test)

    def check_pre_sync(self):
        if not self.url:
            raise ConfigurationException("no hippod server URL specified")

    def sync(self):
        self.check_pre_sync()
        self.user_agent_headers = {'Content-type': 'application/json', 
                                   'Accept': 'application/json' }

        data = None
        full_url = "{}/{}".format(self.url, "api/v1/object")
        request = urllib_request.Request(full_url, data, self.user_agent_headers)
        urllib_request.urlopen(request, timeout=REQUEST_TIMEOUT)



class Test(object):

    class Attachment(object):

        def __init__(self):
            self.references = None
            self.tags = list()
            self.references = list()
            self.responsible = DEFAULT_USERNAME

        def responsible_set(self, name):
            self.responsible = name
        
        def tags_set(self, *tags):
            self.tags = list()
            for tag in tags:
                self.tags.append(tag)
            self._tags_cleanup()

        def tags_add(self, *tags):
            for tag in tags:
                self.tags.append(tag)
            self._tags_cleanup()

        def _tags_cleanup(self):
            # remove duplicate tags in list
            seen = set()
            self.tags = [x for x in self.tags if x not in seen and not seen.add(x)]
        
        def references_set(self, references):
            if type(references) is not list:
                raise ArgumentException("references must be an array, not {}".format(type(references)))
            self.references = references
            self._references_cleanup()

        def references_add(self, *references):
            for reference in references:
                self.references.append(reference)
            self._references_cleanup()

        def _references_cleanup(self):
            # remove duplicate references in list
            seen = set()
            self.references = [x for x in self.references if x not in seen and not seen.add(x)]



    class Achievement(object):

        def __init__(self):
            self.result = DEFAULT_RESULT
            self.test_date = time.strftime("%c")
            self.data = list()
            self.anchor = None

        def result_set(self, result, date=None):
            if date is None:
                date = time.strftime("%c")
            self.result = result
            self.test_data = date

        def anchor_set(self, anchor):
            if type(anchor) is not str:
                raise ArgumentException("anchor must be an string, not {}".format(type(anchor)))
            self.anchor = anchor

        def data_add(self):
            pass

        def construct(self):
            root = dict()
            root["result"] = self.result
            root["test-date"] = self.test_date
            root["data"] = self.data
            return 




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


    def description_set(self, description, type="plain"):
        if (type == "markdown"):
            mime_type = "text/markdown"
        else:
            mime_type = "text/plain"

        # iterate over data structure and if a description
        # is alread there: remove and overwrite
        for i in range(len(self.data)):
            if self.data[i]["type"] == "description":
                del self.data[i]
                break
        data_item = dict()
        data_item["type"] = "description"
        data_item["mime-type"] = mime_type
        data_item["data"] = base64.b64encode(description)


    def title_set(self, title):
        self.title = title

    def categories_set(self, categories):
        if type(categories) is not list or not str:
            raise ArgumentException("categories must be an array or string, not {}".format(type(categories)))
        self.categories = categories



    def json(self):
        root = dict()
        root["submitter"] = self.submitter
        root["achievement"] = list()
        root["achievement"].append(self.achievement)

        # core data elements
        object_item = dict()
        object_item["data"] = self.data

        root["object-item"] = object-item
        return json.dumps(root, sort_keys=True, separators=(',', ': '))



def test_run():        
    c = Core()
    c.set_url("http://lx-02-06")

    t = Test()
    t.attachment.responsible = ""
    t.attachment.tags_add("foo")
    t.attachment.tags_add("foo", "bar")
    t.attachment._tags_cleanup()

    t.achievement.result = ""
    c.add(t)

    c.sync()


if __name__ == "__main__":
    sys.stderr.write("Python client library to interact with HippoD\n")
    sys.stderr.write("Please import this file and use provided function\n")
    sys.stderr.write("Execute Test Suite Now\n\n")
    test_run()
