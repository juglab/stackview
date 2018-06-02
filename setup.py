import os
from setuptools import setup, find_packages

# exec (open('version.py').read())

setup(name='stackview',
      version='0.0.1',
      description='Stack(img) for viewing slices of ndarrays w ndim > 2.',
      # url='https://github.com/maweigert/spimagine',
      author='Coleman Broaddus',
      author_email='broaddus@mpi-cbg.de',
      license='BSD 3-Clause License',
      packages=['stackview'],
      # packages=find_packages(),
      # zip_safe=False)
      )
