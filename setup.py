from setuptools import setup, find_packages

setup(
    name="Greengraph",

    version="0.1.1",

    description="Generates a rough graph of the amount of greenery between two locations",

    url='https://github.com/UCL/rsd-engineeringcourse',

    author='MPHYG001, Thao Le',

    packages=find_packages(exclude=['*test','docs']),

    scripts=['scripts/graph'],

    entry_points={'console_scripts': ['greengraph=greengraph.command:process']},

    install_requires=['argparse','numpy','geopy','matplotlib','requests','csv'],

    license="MIT",

    classifiers=[
        'License :: MIT License',
        'Intended Audience :: MPHYG001 Markers',
        'Programming Language :: Python :: 2.7',

    ]
)