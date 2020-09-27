from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='file-storage-API',
    version='0.1',
    description='API to upload, download, and delete files',
    license="MIT",
    long_description=long_description,
    include_package_data=True,
    package_dir={"": "file_api"},
    packages=find_packages(),
    python_requires='>=3.6',
    scripts=['file_api/app.py'],
    install_requires=[
        'aniso8601==8.0.0',
        'astroid==2.4.2',
        'attrs==20.2.0',
        'certifi==2020.6.20',
        'chardet==3.0.4',
        'click==7.1.2',
        'docutils==0.16',
        'Flask==1.1.2',
        'Flask-RESTful==0.3.8',
        'gunicorn==20.0.4',
        'idna==2.10',
        'importlib-metadata==1.7.0',
        'iniconfig==1.0.1',
        'isort==5.5.2',
        'itsdangerous==1.1.0',
        'Jinja2==2.11.2',
        'lazy-object-proxy==1.4.3',
        'lockfile==0.12.2',
        'MarkupSafe==1.1.1',
        'mccabe==0.6.1',
        'more-itertools==8.5.0',
        'packaging==20.4',
        'pluggy==0.13.1',
        'py==1.9.0',
        'pylint==2.6.0',
        'pyparsing==2.4.7',
        'pytz==2020.1',
        'requests==2.24.0',
        'six==1.15.0',
        'toml==0.10.1',
        'typed-ast==1.4.1',
        'urllib3==1.25.10',
        'Werkzeug==1.0.1',
        'wrapt==1.12.1',
        'zipp==3.1.0',
    ]
    )