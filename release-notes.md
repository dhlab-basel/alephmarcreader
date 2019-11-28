# Release Notes


## Version 1.1.0

### Overview
Apart from minimal changes like typos, this minor release v1.1.0 is mostly concerned with allowing correspondents to be both persons and organisations.

This is done by introducing an abstract class `Correspondent`. Both `Person` and `Organisation` are implementations of this class.

### API changes
* the type of `Correspondent` can be checked by calling `get_type()` which returns either `'Person'` or `'Organisation'`.
* `get_author()` returns `Correspondent` instead of `Person`.
* `get_recipient()` returns `Correspondent` instead of `Person`.
* `get_recipient_organisation()` is redundant and has been removed.



## Version 1.0.0
V.1.0.0 is the initial release of `alephmarcreader`.

For further information and a usage example, see `README.md`.

For an exhaustive list of the API, use `pydoc`, as described in `README.md`.
