from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()
    #remove url
    required.pop(0)
    #remove comments python_version
    requirements = list(map(lambda x: x.split(';')[0], required))

setup(
    name="pygaelo",
    version="0.0.1",
    author="Pixilib",
    url="https://github.com/Pixilib/pygaelo",
    python_requires="~=3.12",
    description="Librairie to communicate with GaelO APIs",
    packages=find_packages(where='src'),    # List of all python modules to be installed
    install_requires=requirements,
    package_dir={"": "src"}
)
