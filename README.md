# PYGSM7
![License](https://img.shields.io/github/license/alvinmurimi/pygsm7)
![PyPI Downloads](https://img.shields.io/pypi/dm/pygsm7)
![Version](https://img.shields.io/pypi/v/pygsm7)

pygsm7 is a Python package that provides functions for encoding and decoding messages using GSM 7-bit encoding. It is designed to facilitate the processing of text messages in the context of SMS and mobile communication.

It also provides two text-encoding workflows that are common in SMS and modem projects:

- Full-Unicode hex encoding and decoding through `pygsm7.encode()` and `pygsm7.decode()`
- True packed GSM 03.38 7-bit encoding and decoding through `pygsm7.encode_gsm7()` and `pygsm7.decode_gsm7()`

## Features

- Round-trip full Unicode text, including emoji and control characters, as uppercase UTF-16BE hex
- Encode and decode packed GSM 7-bit payloads using the GSM 03.38 default and extension tables
- Keep the API small and easy to use for scripts, modem integrations, and SMS tooling

## Installation

Install `pygsm7` with `pip`:

```bash
pip install pygsm7
```

## Usage

### Unicode Hex

Use `encode()` and `decode()` when you need full Unicode coverage.

```python
import pygsm7

encoded = pygsm7.encode("Hello \\U0001F600")
decoded = pygsm7.decode(encoded)

print(encoded)
print(decoded)
```

### GSM 7-Bit

Use `encode_gsm7()` and `decode_gsm7()` for packed GSM 03.38 payloads.

```python
import pygsm7

packed = pygsm7.encode_gsm7("Hello {world} \\u20AC")
decoded = pygsm7.decode_gsm7(packed)

print(packed)
print(decoded)
```

## Contributing

Pull requests and issues are welcome. Refer to [CONTRIBUTING.md](./CONTRIBUTING.md).

## Security Vulnerabilities

If you discover a security vulnerability, please send an e-mail to alvinmayende@gmail.com.

## License

This package is open-source software licensed under the [MIT license](LICENSE.md).
