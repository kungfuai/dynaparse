import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

install_requires = [
    "typeguard==2.10.0",
    "numpy==1.19.2",
    "pydantic==1.8",
    "pyyaml==5.3.1",
]

setup(
    name="dynaparse",
    version="0.1a1",
    author="KUNGFU.AI",
    author_email="michael@kungfu.ai",
    description=(
        "Library enabling dynamic configuration of scripts, especially for machine learning applications"
    ),
    url="https://github.com/kungfuai/dynaparse",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["dynaparse = dynaparse.console:main"],
    },
    include_package_data=True,
    download_url="",
    install_requires=install_requires,
    classifiers=classifiers,
    zip_safe=False,
)
