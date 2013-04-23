from setuptools import setup, find_packages

# read the pip requirements file
requires = [x.strip() for x in open('requirements.txt').readlines()]

setup(
    name='my_closet',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires
)