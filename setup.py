from setuptools import setup, find_packages
from cql_builder import __version__

def readme():
      with open("README.rst") as f:
            return f.read()

setup(name='cql-builder',
      version=__version__,
      description="CQL generation tool",
      long_description=readme(),
      classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License'
      ],
      keywords='',
      author='Jonathan Jengo',
      author_email='jonathan.jengo@gmail.com',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
