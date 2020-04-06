import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="npdocstring",
    version="0.0.1",
    author="Valentin Iovene",
    author_email="valentin@too.gy",
    description="Generate missing numpydocstrings in your Python code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.too.gy/tgy/npdocstring",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
