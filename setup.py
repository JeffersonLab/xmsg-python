#!/usr/bin/env python
'''
Created on 27-02-2015

@author: royarzun
'''
from distutils.core import setup
from distutils.command.clean import clean
from distutils.command.install import install
from setuptools.command.test import test as TestCommand
from setuptools import find_packages


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        pytest.main(self.test_args)

class xMsgInstall(install):

    def run(self):
        install.run(self)
        c = clean(self.distribution)
        c.all = True
        c.finalize_options()
        c.run()

if __name__== '__main__':
    setup(name='xMsg',
          version='1.0',
          description='xMsg for python',
          author='Vardan Gyurgyan',
          author_email='vardan@jlab.org',
          url='https://claraweb.jlab.org',
          test_suite = "test",
          tests_require=['pytest'],
          cmdclass = {'test': PyTest},
          packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
          install_requires = ['pyzmq>=14.5.0','protobuf>=2.6','mock>=1.0.1'],
          )

