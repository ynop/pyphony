# pyphony
A library to work with phone lexica.

* Read and write lexica from/to a file.
* Convert between different formats


## Installation

Install the latest development version:

```sh
pip install git+https://github.com/ynop/pyphony.git
```

## Development

### Prerequisites

* [A supported version of Python 3](https://docs.python.org/devguide/index.html#status-of-python-branches)

It's recommended to use a virtual environment when developing pyphony.
To create one, execute the following command in the project's root directory:

```
python -m venv .
```

To install pyphony and all it's dependencies, execute:

```
pip install -e .
```

### Running the test suite

```
pip install -e .[dev]
python setup.py test
```

With PyCharm you might have to change the default test runner. Otherwise, it might only suggest to use nose. To do so,
go to File > Settings > Tools > Python Integrated Tools (on the Mac it's PyCharm > Preferences > Settings > Tools >
Python Integrated Tools) and change the test runner to py.test.


### Versions

Versions is handled using [bump2version](https://github.com/c4urself/bump2version). To bump the version:

```
bump2version [major,minor,patch,release,num]
```

In order to directly go to a final relase version (skip .dev/.rc/...):

```
bump2version [major,minor,patch] --new-version x.x.x
```

### Release

Commands to create a new release on pypi.

```
rm -rf build
rm -rf dist

python setup.py sdist
python setup.py bdist_wheel
twine upload dist/*
```
