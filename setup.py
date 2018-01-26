from setuptools import setup, find_packages
import re

VERSIONFILE = "eero/version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(name='eero',
      version=verstr,
      description="Manage eero network devices",
      long_description=open("./README.md", "r").read(),
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
      author='Max von Webel',
      author_email='max@343max.de',
      url='https://github.com/343max/eero-client',
      # license='TODO: pick one - MIT License?',
      packages=find_packages(exclude=[
          'ez_setup', 'example', 'tests', 'external']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'requests'
      ]
      )
