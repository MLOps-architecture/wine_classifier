# coding=utf-8
import versioneer
from setuptools import setup, find_packages

packages = find_packages()

with open('requirements.txt') as fp:
    dependencies = fp.readlines()

with open('requirements-test.txt') as fp:
    test_dependencies = fp.readlines()

setup(
    name='awesome_ml',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Project to demo the MLOps architecture',
    author='Data Revenue GmbH',
    author_email='markus@datarevenue.com',
    install_requires=dependencies,
    extras_require={
        'test': test_dependencies,
    },
    packages=packages,
    zip_safe=False,
    include_package_data=True
)
