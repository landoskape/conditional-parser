"""
A simple package to support conditional argument parsing that extends the native argparse packages
ArgumentParser class, works almost identically to the native ArgumentParser class, but with the ability to
use conditional arguments that are only added when a condition is met.

See:
https://github.com/landoskape/conditional-parser
"""

from setuptools import setup

description = "A simple package to support conditional argument parsing."
setup(
    name="conditional-parser",
    version="0.0.1",
    author="Andrew Landau",
    author_email="andrew+tyler+landau+getridofthisanddtheplusses@gmail.com",
    description=description,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=["python code", "compression", "compress"],
    url="https://github.com/landoskape/conditional-parser",
    py_modules=["conditional_parser"],
    license="MIT",
    install_requires=[],
)
