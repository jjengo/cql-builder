from setuptools import setup, find_packages
from cql_builder import __version__

setup(name='cql-builder',
      version=__version__,
      description="CQL generation tool",
      long_description='''
            The cql-builder library is a CQL statement generation tool for Apache Cassandra.
      ''',
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
