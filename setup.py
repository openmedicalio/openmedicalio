import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openmedicalio",
    version="0.0.4",
    author="Open Medical IO",
    author_email="info@openmedical.io",
    description="API client for natural language processing tools by Open Medical IO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/open-medical-io/entities",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
