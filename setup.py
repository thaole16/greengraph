from setuptools import setup, find_packages

setup(
    name = "Greengraph",
    version = "0.1.0",
    packages = find_packages(exclude=['*test']),
    scripts = ['scripts/graph'],
    entry_points = {'console_scripts': ['greengraph=greengraph.command:process']},
    install_requires = ['argparse','numpy','geopy','matplotlib'],
    description = "Generates a rough graph of the amount of greenery between two locations",
    license = "MIT"
)