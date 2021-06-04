import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="queuemining4pm4py",
    version="0.1",
    author="Process Conformance Checking in Python (SS21) Group Queue Mining",
    description="Implements some queue mining functionality, intended to be used with PM4PY",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phihei/Queue_Mining",
    project_urls={
        "Bug Tracker": "https://github.com/phihei/Queue_Mining/issues",
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