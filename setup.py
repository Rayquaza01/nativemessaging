#!/usr/bin/env python3
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name="nativemessaging",
      version="1.0.1",
      description="A package with basic native messaging apis for webextensions",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/Rayquaza01/nativemessaging",
      author="Rayquaza01",
      author_email="rayquaza01@outlook.com",
      license="MPL 2.0",
      packages=["nativemessaging"],
      scripts=["bin/nativemessaging-install.py"],
      include_package_data=True,
      package_data={"": ["README.md"]},
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
          "Operating System :: OS Independent"
      ])
