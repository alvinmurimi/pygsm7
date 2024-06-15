# PYGSM7

pygsm7 is a Python package that provides functions for encoding and decoding messages using GSM 7-bit encoding. It is designed to facilitate the processing of text messages in the context of SMS and mobile communication.

## Features

- Encode text messages into GSM 7-bit format.
- Decode GSM 7-bit encoded messages into readable text.
- Handle special characters commonly used in text messages.
- Convert between Unicode and GSM 7-bit character sets.

## Installation

You can install pygsm7 using `pip`:

```bash
pip install pygsm7
```

## Usage

Here's how to use pygsm7 in your Python code:

```
from pygsm7 import encodeMessage, decodeMessage

# Encoding a text message into GSM 7-bit format
encoded_message = encodeMessage("Hello, world!")

# Decoding a GSM 7-bit encoded message
decoded_message = decodeMessage(encoded_message)

print("Encoded Message:", encoded_message)
print("Decoded Message:", decoded_message)

```

## GSM 7-bit Character Tables
This module includes predefined GSM 7-bit character tables and handling of special characters. You can customize the character tables and special characters to suit your needs.

### Contributing
Pull requests and issues are welcome. Refer to [CONTRIBUTING.md](./CONTRIBUTING.md)

### Security Vulnerabilities
If you discover any security vulnerability, please send an e-mail to alvinmayende@gmail.com.

### License
This package is open-source software licensed under the [MIT license](LICENSE.md).
