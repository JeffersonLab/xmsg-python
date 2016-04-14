#!/usr/bin/env python
# coding=utf-8

import os

from distutils.core import setup, Command
from distutils.command.clean import clean
from distutils.command.install import install
from setuptools.command.test import test as TestCommand
from setuptools import find_packages
import xmsg


class XMsgTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        pytest.main(self.test_args)


class XMsgClean(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


class XMsgInstall(install):

    def run(self):
        install.run(self)
        c = clean(self.distribution)
        c.all = True
        c.finalize_options()
        c.run()

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme_file:
    README = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), 'LICENSE')) as license_file:
    LICENSE = license_file.read()

if __name__ == '__main__':
    setup(name='xmsg',
          version=xmsg.__version__,
          description='xMsg a lightweight, publish/subscribe messaging system',
          long_description=README,
          license=LICENSE,
          author='Vardan Gyurgyan, Ricardo Oyarzun',
          author_email='vardan@jlab.org',
          platforms=['OSX', 'Linux'],
          url='https://claraweb.jlab.org',
          test_suite="tests",
          cmdclass={
            'test': XMsgTest,
            'clean': XMsgClean,
          },
          packages=find_packages(exclude=["tests.*", "tests"]),
          scripts=['bin/unix/px_node',
                   'bin/unix/px_proxy',
                   'bin/unix/px_publisher',
                   'bin/unix/px_subscriber',
                   'bin/unix/px_sync_publisher'],
          classifiers=[
              'Intended Audience :: Developers',
              'Programming Language :: Python',
              'Programming Language :: Python :: 2.6',
              'Programming Language :: Python :: 2.7'],
          )
