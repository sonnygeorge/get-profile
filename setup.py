from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.2"
DESCRIPTION = "Quickly profile your code with a single line of code."
LONG_DESCRIPTION = "A simple library to inject the most profiling bang-for-buck into a single line of code (decorator)."


setup(
    name="get-profile",
    version=VERSION,
    author="Sonny George",
    author_email="<sonnygeorge5@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=["pandas", "numpy"],
    keywords=["python", "profiling", "profile", "runtime", "decorator", "cprofile"],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
