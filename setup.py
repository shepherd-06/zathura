from setuptools import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(name='Logbook',  # alternative name docket
      version='0.4',
      description='Hello World',
      url='https://github.com/ibtehaz-shawon/LoggerProject',
      author='Ibtehaz Shawon',
      author_email='ibtehaz.92@gmail.com',
      license='MIT',
      packages=['LoggerProject'],
      install_requires=[
            install_requires
      ],
      entry_points={
        'console_scripts': [
            'Logbook = LoggerProject.__init__:create_app'
        ]
        },
       classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
      zip_safe=False)
