

install2:
	pip install -e . --no-deps

install3:
	pip3 install -e . --no-deps

test2:
	python setup.py test

test3:
	python3 setup.py test

test: test2 test3

upload:
	python setup.py sdist upload -r pypi
