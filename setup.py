from setuptools import setup, find_packages
import os

current = os.getcwd()

setup(
    name='FairMongo',
    version='1.2.0',
    description='A complete Python Package for PyMongo and MongoDB.',
    url='https://github.com/chazzcoin/FairMongo',
    author='ChazzCoin',
    author_email='chazzcoin@gmail.com',
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=['pymongo~=3.12.3', 'FCoRE~=1.0.4'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ]
)