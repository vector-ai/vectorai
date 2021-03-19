#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

core_req = ["requests", "numpy", "pandas", "appdirs>=1.4.4", "tqdm>=4.27.0", "plotly>=4.0.0"]
extras_req = {
    "dev" : ["twine", "black", "pytest", "pytest-cov", "vectorai", "openapi-to-sdk"],
    "test" : ["pytest", "pytest-cov", "pytest-rerunfailures"],
    "docs" : ["sphinx-rtd-theme>=0.5.0", "nbsphinx>=0.7.1"]
}
extras_req["all"] = [p for r in extras_req.values() for p in r]

version = '0.2.5'
if 'IS_VECTORAI_NIGHTLY' in os.environ.keys():
    from datetime import datetime
    name = 'vectorai-nightly'
    version = version + '.' + datetime.today().date().__str__().replace('-', '.') 
else:
    name = 'vectorai'

setup(
    name=name,
    version=version,
    author="OnSearch Pty Ltd",
    author_email="dev@vctr.ai",
    description="A Python framework for building vector based applications. Encode, query and analyse data using vectors.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords="vector, embeddings, machinelearning, ai, artificialintelligence, nlp, tensorflow, pytorch, nearestneighbors, search, analytics, clustering, dimensionalityreduction",
    url="https://github.com/vector-ai/vectorai",
    license="Apache",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3",
    install_requires=core_req,
    extras_require=extras_req,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Database",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Multimedia :: Sound/Audio :: Conversion",
        "Topic :: Multimedia :: Video :: Conversion",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Recognition",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
