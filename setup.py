

# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os.path as osp
import glob


with open('rximg/requirements.txt', encoding="utf-8-sig") as f:
    requirements = f.readlines()
    requirements = [r.strip() for r in requirements]
    # requirements.append('tqdm')
print('get requirements:', requirements)
setup(
    name="rximg",
    version="0.1.0",
    description="rximg package",
    license="MIT License",
    author="rximg",
    # package_dir={"rximg":"./rximg"},
    install_requires=requirements,
    packages=find_packages(where="."),
    include_package_data=True,
    # package_data={"":["LICENSE","requirements.txt",'*.md'],
    #     "frontend": ["./frontend/dist/*.html","./frontend/dist/assets/*.js","./frontend/dist/assets/*.css"]},
    # data_files=[("frontend",frontends),
    #     ("configs",configs),
    #     ("",['__init__.py','LICENSE','requirements.txt','README.md','app.py'])],
    # include_package_data=True,
    long_description="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.9"
)