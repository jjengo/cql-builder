from setuptools import setup, find_packages

setup(name='cql-builder',
      version='0.0.1',
      description="Generic data modeling and validation",
      long_description=""" """,
      classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License'
      ],
      keywords='',
      author='Jonathan Jengo',
      author_email='jonathan.jengo@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'cassandra-driver>=2.1.0'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
