#!/usr/bin/env python
# coding=utf-8

import os

from setuptools import setup, Command
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
        os.system('rm -vrf ./.cache ./.eggs ./build ./dist')
        os.system('rm -vrf ./*.tgz ./*.egg-info')
        os.system('find . -name "*.pyc" -exec rm -vrf {} \;')
        os.system('find . -name "__pycache__" -exec rm -rf {} \;')


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
          scripts=['xmsg/scripts/unix/px_node',
                   'xmsg/scripts/unix/px_proxy',
                   'xmsg/scripts/unix/px_publisher',
                   'xmsg/scripts/unix/px_subscriber',
                   'xmsg/scripts/unix/px_sync_publisher'],
          classifiers=[
              'Intended Audience :: Developers',
              'Programming Language :: Python',
              'Programming Language :: Python :: 2.6',
              'Programming Language :: Python :: 2.7'],
          )
