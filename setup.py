from setuptools import setup

setup(name="systeminfo",
      version="0.1",
      description="First scrape of Bike data",
      url="",
      author="Stephen Edwards",
      licence="GPL3",
      install_requires=['requests'],
      packages=['systeminfo'],
      entry_points={
        'console_scripts':['bikeScrape=systeminfo.main:main']
        }
      )
