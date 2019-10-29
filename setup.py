from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

short_description = "Zathura is the utility package of bugtracker. Check https://github.com/p1r-a-t3/Bugtracker for details"


install_requires = [
    'pyfiglet',
]

setup(name='zathura',
      packages=['ZathuraProject'],
      version='0.0.6.0b1',
      description='',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/p1r-a-t3/zathura',
      author='Mr Anderson',
      author_email='ibtehaz.shawon@gmail.com',
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
