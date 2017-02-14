# -*- coding: utf-8 -*-

import sys


if sys.version_info < (3, 0):
    from hippodclient import Test
    from hippodclient import Container
else:
    from hippodclient.hippodclient import Test
    from hippodclient.hippodclient import Container


