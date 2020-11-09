#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['dnspython==2.0.0', 'paho-mqtt==1.5.1']

setup_requirements = []

test_requirements = [ ]

setup(
    author="Kevin Van Wilder",
    author_email='kevin@van-wilder.be',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    entry_points={
        'console_scripts': [
            'nhc_hobby_api=nhc_hobby_api.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='nhc_hobby_api',
    name='nhc_hobby_api',
    packages=find_packages(include=['nhc_hobby_api', 'nhc_hobby_api.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/kevwilde/nhc_hobby_api',
    version='0.1.0',
    zip_safe=False,
)
