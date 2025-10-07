# setup.py

from setuptools import setup, find_packages

setup(
    name="steinernet",
    version="0.1.1",
    description="Steiner Tree Library for Python",
    author="Afshin Sadeghi",
    packages=find_packages(),
    install_requires=[
        "networkx>=2.0"
    ],
    python_requires=">=3.7",
    url="https://github.com/afshinsadeghi/steinernetpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
