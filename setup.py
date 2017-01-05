from setuptools import setup, find_packages

setup(
    name="Greengraph",

    version="1.0.0",

    description="Generates a rough graph of the amount of greenery between two locations",
    long_description=open('README.md').read(),

    url='https://github.com/thaole16/greengraph',

    author='MPHYG001, Thao Le',
    author_email='thao.le.16@ucl.ac.uk',

    packages=find_packages(exclude=['*test','docs']),

    scripts=['scripts/graph'],

    entry_points={'console_scripts': ['greengraph=greengraph.command:process']},

    install_requires=['argparse','numpy','geopy','matplotlib','requests'],

    license="MIT",

    classifiers=[
        'License :: MIT License',
        'Intended Audience :: MPHYG001 Markers',
        'Programming Language :: Python :: 2.7',

    ]
)