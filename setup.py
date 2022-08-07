

# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

import glob

frontends = glob.glob('frontends/dist/*')+glob.glob('frontends/dist/*/*')

setup(
    name="rximg",
    version="0.1.0",
    description="rximg package",
    license="MIT License",
    author="rximg",
    packages=find_packages(where='../rximg'),
    package_dir={"": "../rximg"},
    package_data={"":["LICENSE","requirements.txt",'*.md'],"frontend": ["./frontend/dist/*.html","./frontend/dist/assets/*.js","./frontend/dist/assets/*.css"]},
    # data_files=[("frontend",frontends)],
    include_package_data=True,
    long_description="",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
    ]
)