from setuptools import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(name='Docket',  # alternative name docket
      packages = ['DocketProject'],
      version='0.5',
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
