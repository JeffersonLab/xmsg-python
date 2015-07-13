#!/usr/bin/env python
'''
 Copyright (C) 2015. Jefferson Lab, xMsg framework (JLAB). All Rights Reserved.
 Permission to use, copy, modify, and distribute this software and its
 documentation for educational, research, and not-for-profit purposes,
 without fee and without a signed licensing agreement.

 Author Vardan Gyurjyan
 Department of Experimental Nuclear Physics, Jefferson Lab.

 IN NO EVENT SHALL JLAB BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
 INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
 THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF JLAB HAS BEEN ADVISED
 OF THE POSSIBILITY OF SUCH DAMAGE.

 JLAB SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 PURPOSE. THE CLARA SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED
 HEREUNDER IS PROVIDED "AS IS". JLAB HAS NO OBLIGATION TO PROVIDE MAINTENANCE,
 SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
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


if __name__ == '__main__':
    setup(name='xMsg',
          version='2.0',
          description='xMsg for python',
          author='Vardan Gyurgyan',
          author_email='vardan@jlab.org',
          url='https://claraweb.jlab.org',
          test_suite="tests",
          tests_require=['pytest', 'mockito'],
          cmdclass={'test': PyTest},
          packages=find_packages(exclude=["*.tests", "*.tests.*",
                                          "tests.*", "tests"]),
          install_requires=['pyzmq>=14.5.0', 'protobuf>=2.6', 'mock>=1.0.1',
                            'enum34>=1.0.4', 'argparse>=1.2.1', 'netifaces>=0.10.4']
          )
