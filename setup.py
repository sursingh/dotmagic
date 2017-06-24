#!/usr/bin/env python

from distutils.core import setup

setup(name='dotmagic',
        version='1.0',
        description='Graphviz magic for ipython',
        author='Surinder Singh',
        author_email='sursingh@gmail.com',
        packages=['dotmagic'],
        package_data={
            'dotmagic': [ '*.xsl' ]
        },
        include_package_data=True,
     )
