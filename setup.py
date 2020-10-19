# -*- coding: utf-8 -*-

# Terceiros
from setuptools import find_packages, setup

__version__ = '0.1.0'
__description__ = 'Api test to Boa Vista Interview'
__long_description__ = ''

__author__ = 'Dheinny Marques'
__author_email__ = 'dheinny@gmail.com'

setup(
    name='api',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    packges=find_packages(),
    license='MIT',
    description=__description__,
    long_description=__long_description__,
    url='https://github.com/dheinny',
    keywords='API, CRUD',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Interviewers',
        'Operation System :: OS Independent',
        'Topic :: Software Development',
        'Enviroment :: Web Enviroment',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
    ],
)

