import pathlib
import re
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

with (HERE / "proximl" / "__init__.py").open() as fp:
    try:
        version = re.findall(r'^__version__ = "([^"]+)"\r?$', fp.read(), re.M)[
            0
        ]
    except IndexError:
        raise RuntimeError("Unable to determine version.")

README = (HERE / "README.md").read_text()

with (HERE / "requirements.txt").open() as fp:
    install_requires = fp.read().splitlines()


setup(
    name="proximl",
    version=version,
    description="proxiML client SDK and command line utilities",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/proxiML/python-sdk",
    author="proxiML",
    author_email="support@proximl.ai",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
        proximl=proximl.cli:cli
    """,
)