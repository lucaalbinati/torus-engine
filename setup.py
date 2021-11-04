import setuptools

setuptools.setup(
    name="torus-engine",
    version="0.1.0",
    author="Luca Albinati",
    author_email="luca.albinati@gmail.com",
    description="3D ASCII character rendering engine",
    url="https://github.com/lucaalbinati/Torus",
    project_urls={
        "Bug Tracker": "https://github.com/lucaalbinati/Torus/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)