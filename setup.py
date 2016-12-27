from setuptools import setup, find_packages

setup(
    name = "Greengraph",
    version = "0.1.0",
    packages = find_packages(exclude=['*test']),
    scripts = ['scripts/graph'],
    install_requires = ['argparse']
	description= "Generates a rough graph of the amount of greenery between two locations"
	license = "MIT"
)