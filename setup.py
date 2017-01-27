from setuptools import setup

version = "0.1.0"
readme = open('README.rst').read()

setup(name="jobarchitect",
      version=version,
      long_description=readme,
      packages=["jobarchitect"],
)
