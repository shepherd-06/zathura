from setuptools import setup

# with open('requirements.txt') as fp:
#     install_requires = fp.read()

install_requires = [
    'astroid==2.1.0',
    'bleach==3.1.0',
    'certifi==2018.11.29',
    'chardet==3.0.4',
    'docutils==0.14',
    'gitdb2==2.0.5',
    'GitPython==2.1.11',
    'idna==2.8',
    'isort==4.3.4',
    'lazy-object-proxy==1.3.1',
    'mccabe==0.6.1',
    'peewee==3.8.1',
    'pkginfo==1.5.0.1',
    'Pygments==2.3.1',
    'pylint==2.2.2',
    'pymongo==3.7.2',
    'pytz==2018.7',
    'readme-renderer==24.0',
    'requests==2.21.0',
    'requests-toolbelt==0.8.0',
    'six==1.12.0',
    'smmap2==2.0.5',
    'tqdm==4.29.1',
    'twine==1.12.1',
    'typed-ast==1.2.0',
    'urllib3==1.24.1',
    'webencodings==0.5.1',
    'wrapt==1.11.1',
]


setup(name='Docket',  # alternative name docket
      packages = ['DocketProject'],
      version='0.6',
      description='Hello World',
      url='https://github.com/ibtehaz-shawon/Docket',
      author='Ibtehaz Shawon',
      author_email='ibtehaz.92@gmail.com',
      license='MIT',
      install_requires=[
            install_requires
      ],
      entry_points={
        'console_scripts': [
            'Docket = DocketProject.__init__:create_app'
        ]
        },
       classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
      zip_safe=False)
