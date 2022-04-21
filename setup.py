import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="git-relevant-history",
    version="1.0.1",
    description="Extract subproject with just the relevant history",
    long_description="README.md",
    long_description_content_type="text/markdown",
    url="https://github.com/rainlabs-eu/git-relevant-history",
    author="Rainlabs",
    author_email="github@rainlabs.pl",
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["docopt"],
    entry_points={
        "console_scripts": [
            "git-relevant-history=gitrelevanthistory.main:main",
        ]
    },
)