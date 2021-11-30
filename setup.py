import os
import setuptools

rootdir = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(rootdir, 'README.md')).read()

setuptools.setup(
    name="torus-engine",
    version="1.1.3",
    author="Luca Albinati",
    author_email="luca.albinati@gmail.com",
    description="3D ASCII character rendering engine",
    long_description = long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/lucaalbinati/torus-engine",
    project_urls={
        "Bug Tracker": "https://github.com/lucaalbinati/torus-engine/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)