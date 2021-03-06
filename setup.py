#! /usr/bin/env python3.6

from setuptools import setup, find_packages

setup(name="saltbot",
      version="0.1",
      packages=find_packages(exclude=['*.tests', '*.tests.*',
                                      'tests.*', 'tests']),
      package_dir={'saltbot': 'saltbot'},
      url='https://github.com/jandersen7/saltybettor',
      author="John Andersen",
      author_email="johnandersen185@gmail.com",
      scripts=['saltbot/scripts/saltbot'],
      description="A bot for placing bets on [SaltyBet](https://www.saltybet.com), running off of selenium and the Gmail API (email alerts).",
      install_requires=['selenium>=3.3.3', 'beautifulsoup4>=4.7.1', 'requests>=2.2.1', 'psycopg2>=2.8.3'],
      keywords=['saltybet', 'MUGEN'])
