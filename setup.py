from setuptools import setup, find_packages
import os.path
import re

VERSIONFILE = "eero/version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

README_FILE = next(
    r
    for r in ['./README.md', './README.txt', './README']
    if os.path.isfile(r)
)

setup(name='eero',
      version=verstr,
      description="Manage eero network devices",
      long_description=open(README_FILE, "r").read(),
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Utilities",
          "License :: OSI Approved :: MIT License",
      ],
      keywords='eero',
      author='Bruce McIntyre',
      author_email='bruce.mcintyre@gmail.com',
      url='https://github.com/bruskiza/eero-client',
      license='MIT License',
      packages=find_packages(exclude=[
          'ez_setup', 'example', 'tests', 'external']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'requests'
      ]
      )
