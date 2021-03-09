import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
]

install_requires = [
    "imagehash>=4.0,<5.0",
    "numpy>=1.17.3",
    "pillow>=6.2.2,<7.0",
    "PTable>=0.9.2,<1.0",
    "torch>=1.3.0,<2.0",
    "torchvision>=0.4.1,<1.0",
    "tqdm>=4.37.0",
    "typing>=3.7",
    "pandas",
]

setup(
    name="dynaparse",
    version="0.1",
    author="KUNGFU.AI",
    author_email="michael@kungfu.ai",
    description=("Module for enabling dynamic configuration of scripts"),
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
