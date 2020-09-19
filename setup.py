from setuptools import setup, find_packages

with open("readme.md", 'r') as f:
    long_description = f.read()

setup(
    name='file-storage-API',
    version='0.1',
    description='API to upload, download, and delete files',
    license="MIT",
    long_description=long_description,
    author='ptrwn',
    author_email='1374688@gmail.com',
    url = 'https://github.com/ptrwn/http_fs',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "file_api"},
    packages=find_packages(),
    )