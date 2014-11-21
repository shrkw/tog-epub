#!/bin/env python
# encoding: UTF-8

from __future__ import division, print_function, absolute_import
from setuptools import Command, setup
from togepub import __version__

setup(
    name='togepub',
    version=__version__,
    url='',
    license='MIT License',
    author='Hiroyuki Shirakawa',
    author_email='shrkwh@gmail.com',
    description='generate EPUB from togetter site',
    long_description='Refer to README',
    packages=['togepub'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Customer Service',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    scripts = ['main.py'],
    entry_points='''
        [console_scripts]
    '''
)
