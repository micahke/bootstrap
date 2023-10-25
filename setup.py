from setuptools import setup, find_packages
  
setup(
    name='bootstrap',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bootstrap = script.main:main',   
        ],
    },
    install_requires=[
        req.strip() for req in open('requirements.txt').readlines()
    ],
)
