from setuptools import setup

with open('LoggerProject/requirements.txt') as fp:
    install_requires = fp.read()

setup(name='Logbook',
      version='0.2',
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
      zip_safe=False)
