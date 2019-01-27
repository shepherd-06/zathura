from setuptools import setup

install_requires = [
    'astroid',
    'bleach',
    'certifi',
    'chardet',
    'docutils',
    'gitdb2',
    'GitPython',
    'idna',
    'isort',
    'lazy-object-proxy',
    'mccabe',
    'peewee',
    'pkginfo',
    'Pygments',
    'pylint',
    'pymongo',
    'pytz',
    'readme-renderer',
    'requests',
    'requests-toolbelt',
    'six',
    'smmap2',
    'tqdm',
    'twine',
    'typed-ast',
    'urllib3',
    'webencodings',
    'wrapt',
]


setup(name='Zathura',  # alternative name docket
      packages = ['ZathuraProject'],
      version='0.7.2.dev1',
      description='Zathura is a small space logger. It logs stuff into her logbook as she drifts into vast unknown of development phase.',
      url='https://github.com/ibtehaz-shawon/Zathura',
      author='Ibtehaz Shawon',
      author_email='ibtehaz.92@gmail.com',
      license='MIT',
      install_requires=[
            install_requires
      ],
      entry_points={
        'console_scripts': [
            'Zathura = ZathuraProject.__init__:create_app'
        ]
        },
       classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
      zip_safe=False)
