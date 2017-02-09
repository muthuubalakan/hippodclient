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
      classifiers=[
			'Development Status :: 4 - Beta',

			'Intended Audience :: Developers',
			'Topic :: Software Development :: Build Tools',

             'License :: OSI Approved :: MIT License',

			'Programming Language :: Python :: 2',
			'Programming Language :: Python :: 2.6',
			'Programming Language :: Python :: 2.7',
			'Programming Language :: Python :: 3',
			'Programming Language :: Python :: 3.2',
			'Programming Language :: Python :: 3.3',
			'Programming Language :: Python :: 3.4',
		],
      zip_safe=False
     )
