from setuptools import setup

setup(name="GetData",
      version="0.1",
      description="Bike and Weather Data scrape",
      url="https://github.com/seddie95/comp30830",
      author="Group 3: Alice Moyon, Dennis Kroner,Stephen Edwards",
      licence="GPL3",
      install_requires=['requests', 'mysql-connector-python'],
      packages=['GetData'],
      entry_points={
          'console_scripts': ['bikeScrape=GetData.main:main']
      }
      )
