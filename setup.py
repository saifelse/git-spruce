from __future__ import absolute_import

from setuptools import setup

setup(
    name="git-spruce",
    version="0.1.0",
    description="Git command to update multiple branches / PRs",
    install_requires=["click>=7.0"],
    packages=["spruce"],
    scripts=['bin/git-spruce'],
)
