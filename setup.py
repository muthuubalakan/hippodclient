from setuptools import setup

setup(name='hippodclient',
      version='0.1',
      description='CLient Adapter to HippodD',
      url='http://github.com/hgn/hippod-client',
      author='Hagen Paul Pfeifer',
      author_email='hagen@jauu.net',
      license='MIT',
      packages=['hippodclient'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False
     )
