# coding=utf-8
import logging
import subprocess
from setuptools import setup, find_packages

packages = find_packages()


def no_private(dependencies):
    public_pkgs = [x.split("#")[0].strip() for x in dependencies if "# private" not in x]
    return public_pkgs


with open("requirements.txt") as fp:
    dependencies = fp.readlines()


setup(
    name="wine_classifier",
    version="0.1",
    description="Wine classifier project for MLOps demo",
    author="Data Revenue GmbH",
    author_email="pedro@datarevenue.com",
    install_requires= no_private(dependencies),
    packages=packages,
    zip_safe=False,
    include_package_data=True,
)
