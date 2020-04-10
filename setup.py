from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRES = open('requirements.txt', 'r').read()

setup(name='optimized-options-portfolio',
      version='0.0.1',
      author='Juhi Chandalia',
      author_email='jkchandalia@gmail.com',
      description=long_description,
      url='http://github.com/jkchandalia/optimized-options-portfolio',
      packages=find_packages(),
      install_requires=REQUIRES,
      summary='Short options portfolio tools',
      license='MIT',
      )