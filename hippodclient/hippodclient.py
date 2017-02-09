# -*- coding: utf-8 -*-

import json
import pprint
import base64
import re
import os
import sys
import time
import mimetypes
import ConfigParser
import StringIO
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

DEFAULT_USERNAME = "anomymous"


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
            self.responsible = DEFAULT_USERNAME
        
        def tags_set(self, tags):
            if type(tags) is not list:
                raise ArgumentException("data must be an array, not {}".format(type(tags)))
            self.tags = tags
            self._tags_cleanup()

        def tags_add(self, *tags):
            for tag in tags:
                self.tags.append(tag)
            self._tags_cleanup()

        def _tags_cleanup(self):
            # remove duplicate tags in list
            seen = set()
            self.tags = [x for x in self.tags if x not in seen and not seen.add(x)]



    class Achievement(object):
        def __setattr__(self, name, value):
            object.__setattr__(self, name, value)


    def init_defaults(self):
        self.submitter = DEFAULT_USERNAME
        self.categories = None
        self.data = list()

    def __init__(self):
        self.init_defaults()
        self.attachment = Test.Attachment()
        self.achievement = Test.Achievement()

                




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