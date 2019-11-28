# alephmarcreader
## General
Python library to read Marc obtained from Aleph, the catalogue of the library of the University of Basel.

This library supports Marc21, MARCXML, and AlephX.

## Documentation
The docstrings can be displayed with pydoc (from the project root): `pydoc alephmarcreader.abstractalephmarcreader.AbstractAlephMarcReader
`. For the inner classes such as `Person`, run `pydoc alephmarcreader.abstractalephmarcreader.AbstractAlephMarcReader.Person`.

## Design
`alephmarcreader.abstractalephmarcreader.AbstractAlephMarcReader` provides methods to access Marc data.
It is an abstract class that has two abstract methods `__get_field` and `__get_subfield_text` that have to be implemented in the subclass for the file format at hand.

## Unit Tests

From the project root, run `python -m unittest alephmarcreader.tests.test_[Marc[21|XML]|X]Reader`.

## Dependencies

- `pymarc`: install with pip
- `lxml`: install with pip

The library works both with python2 and python3.

## Usage
Install the package with `pip install alephmarcreader`.

Example usage:
```python
# import
from alephmarcreader import AlephMarcXMLReader

# Read data from local file
marc = AlephMarcXMLReader('example_file.xml')

# get some fields
author = marc.get_author()[0]
recipient = marc.get_recipient()[0]
date = marc.get_date()[0]

# print it
print(author.name)
print(recipient.name)
print(date)
```

For an exhaustive list of the API, use `pydoc`, as described above.
