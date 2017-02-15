# Usage

Simple install this module via pip (pip for Python 2 is also supported)

```
pip3 install hippodclient
```

And simple upload test with the following lines:

```
import hippodclient

c = hippodclient.Container(url="http://localhost")

t = hippodclient.Test()
t.submitter_set("anonymous")
t.title_set("random title")
t.categories_set("team:bar")
t.attachment.tags_add("foo", "bar")
t.achievement.result = "passed"

c.add(t)
c.sync()
```

That's it!


# Development

## Installation

This package is python2 and 3 compatible. To check for both version please
install the required dependencies:

For Debian and Python2 Environment

```
sudo apt-get install python-setuptools
```

For Debian and Python3 Environment

```
sudo apt-get install python3-setuptools
```


# Testing

## Python Test Dependencies

```
sudo aptitude install python-tk
```


Python2 Environment

```
python2 setup.py test
```

Python3 Environment

```
python3 setup.py test
```
