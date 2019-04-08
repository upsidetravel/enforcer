# Enforcer: AWS SSM Parameter Store Management CLI
-------------------

# Docs
Helper script to upload secrets to AWS SSM Parameter Store.
Any secrets greater than the AWS Parameter store value limit 4096 characters will be broken up into chunks and suffixed `_chunk_<index>`
This script will read your secret value from the clipboard automagically
- [Chunking logic deep dive](CHUNKS.md)

# Usage
```
pip install -r requirements.txt
python app.py
python app.py upload --env(dev, stg, prod, cent) --region=<aws_region> --fq_secret_key=</secret_directory/secret_name> --secret_value=<secret_value>
```

### Default Usage
[![enforcer-default](https://asciinema.org/a/NiiwxdTfU7tAlktB3TFYw5rIx.svg)](https://asciinema.org/a/NiiwxdTfU7tAlktB3TFYw5rIx)

### Shortcut Usage
[![enforcer-shorcut](https://asciinema.org/a/W4VjnodWKpO6wDt28QJj3gLVD.svg)](https://asciinema.org/a/W4VjnodWKpO6wDt28QJj3gLVD)

# Pyperclip dependency
*Not Implemented Error*
- https://pyperclip.readthedocs.io/en/latest/introduction.html#not-implemented-error

Formatting
==========

This repo includes `yapf`, which will format code to our style. It's currently integrated into the lint step, so `make pep8` will
also reformat code.

Versioning
==========
Uses [semantic versioning](https://semver.org/), expecting that we'll start our
versions at 1.0 (to signal that they're used in production. If they aren't, feel
free to use <1.0).
- MAJOR version when you make incompatible API changes,
- MINOR version when you add functionality in a backwards-compatible manner, and
- PATCH version when you make backwards-compatible bug fixes.

Licenses
====
- [Apache 2.0](LICENSE)
- [3rd party licenses](3RD_PARTY_DEPENDENCIES.md)