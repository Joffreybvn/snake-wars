
# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="snake-wars",
    version="0.1.1",
    description="Snake game implementation for multiplayer and reinforcement learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://snake-wars.readthedocs.io/",
    author="Joffrey Bienvenu",
    author_email="joffreybvn@gmail.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: pygame",
        "Topic :: Games/Entertainment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pygame", "PodSixNet", "iteration-utilities"]
)
