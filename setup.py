from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

install_requires = [
    'peewee',
]
# https://the-hitchhikers-guide-to-packaging.readthedocs.io/en/latest/specification.html

setup(name='zathura',
      packages=['ZathuraProject'],
      version='0.0.4.9.b1',
      description='Zathura is a small space logger. It logs stuff into her logbook as she drifts into vast unknown of development phase.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ibtehaz-shawon/Zathura',
      author='Ibtehaz Shawon',
      author_email='ibtehaz.92@gmail.com',
      license='MIT',
      install_requires=[
          install_requires
      ],
      entry_points={
          'console_scripts': [
              'zathura = ZathuraProject.__init__:create_app'
          ]
      },
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
