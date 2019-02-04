from setuptools import setup

install_requires = [
    'peewee',
]


setup(name='zathura',
      packages = ['ZathuraProject'],
      version='0.0.3.dev7',
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
            'zathura = ZathuraProject.__init__:create_app'
        ]
        },
       classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
      zip_safe=False)
