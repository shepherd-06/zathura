from setuptools import setup

with open('LoggerProject/requirements.txt') as fp:
    install_requires = fp.read()

setup(name='LoggerProject',
      version='0.0.0.1+git',
      description='Hello World',
      url='https://github.com/ibtehaz-shawon/LoggerProject',
      author='Ibtehaz Shawon',
      author_email='ibtehaz.shawon@gmail.com',
      license='MIT',
      packages=['LoggerProject'],
      install_requires=[
            install_requires
      ],
      entry_points={
        'console_scripts': [
            'LoggerP = LoggerProject.__init__:create_app'
        ]
        },
      zip_safe=False)
