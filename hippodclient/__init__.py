# -*- coding: utf-8 -*-

import sys


if sys.version_info <= (3, 0):
    from hippodclient import Test
    from hippodclient import Core
else:
    from hippodclient.hippodclient import Test
    from hippodclient.hippodclient import Core


