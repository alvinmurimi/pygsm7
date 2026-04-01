"""
Helpers for Unicode hex and GSM 7-bit text encoding.

The legacy encode/decode functions continue to expose the modem-friendly
UTF-16BE hex behavior used by this package historically. True GSM 03.38
support is available through the explicit GSM7 helpers.
"""

import re


_HEX_PATTERN = re.compile(r"^[0-9A-Fa-f]+$")
_GSM7_ESCAPE = 0x1B

_GSM7_BASIC_CHARS = (
    "@\u00a3$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ"
    "\x1b"
    "ÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?"
    "¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà"
)

_GSM7_EXTENSION_DECODE_MAP = {
    0x0A: "\f",
    0x14: "^",
    0x28: "{",
    0x29: "}",
    0x2F: "\\",
    0x3C: "[",
    0x3D: "~",
    0x3E: "]",
    0x40: "|",
    0x65: "€",
}

_GSM7_BASIC_DECODE_MAP = dict((index, character) for index, character in enumerate(_GSM7_BASIC_CHARS))
_GSM7_BASIC_ENCODE_MAP = dict((character, index) for index, character in enumerate(_GSM7_BASIC_CHARS))
_GSM7_EXTENSION_ENCODE_MAP = dict(
    (character, index) for index, character in _GSM7_EXTENSION_DECODE_MAP.items()
)

if "\x1b" in _GSM7_BASIC_ENCODE_MAP:
    del _GSM7_BASIC_ENCODE_MAP["\x1b"]

GSM7_Table = ["%04X" % ord(_GSM7_BASIC_DECODE_MAP[index]) for index in range(128)]
GSM7_Table_Extend = [
    "%04X" % ord(_GSM7_EXTENSION_DECODE_MAP[index])
    for index in sorted(_GSM7_EXTENSION_DECODE_MAP)
]

specialChars = ["%04X" % code for code in range(0x20)] + ["007F"]
specialCharsIgnoreWrap = []

__all__ = [
    "encode",
    "decode",
    "encodeMessage",
    "decodeMessage",
    "encode_gsm7",
    "decode_gsm7",
    "encodeGsm7",
    "decodeGsm7",
]


def encodeMessage(message):
    if message is None or message == "":
        return ""
    _ensure_text(message, "message")

    try:
        return message.encode("utf-16-be").hex().upper()
    except UnicodeEncodeError as exc:
        raise ValueError(
            "Message contains invalid Unicode code points and cannot be UTF-16 encoded."
        ) from exc


def decodeMessage(message):
    if message is None or message == "":
        return ""
    compact = _normalize_hex_payload(message, 4, "UTF-16 hex message")

    try:
        return bytes.fromhex(compact).decode("utf-16-be")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "UTF-16 hex message contains invalid or incomplete surrogate data."
        ) from exc


def encode(message):
    return encodeMessage(message)


def decode(message):
    return decodeMessage(message)


def encode_gsm7(message):
    if message is None or message == "":
        return ""
    _ensure_text(message, "message")
    septets = []

    for character in message:
        if character in _GSM7_BASIC_ENCODE_MAP:
            septets.append(_GSM7_BASIC_ENCODE_MAP[character])
        elif character in _GSM7_EXTENSION_ENCODE_MAP:
            septets.append(_GSM7_ESCAPE)
            septets.append(_GSM7_EXTENSION_ENCODE_MAP[character])
        else:
            raise ValueError(
                "Character %r cannot be encoded in the GSM 7-bit alphabet." % character
            )

    return _pack_septets(septets).hex().upper()


def decode_gsm7(message, septet_count=None):
    if message is None or message == "":
        return ""
    compact = _normalize_hex_payload(message, 2, "GSM 7-bit packed hex")
    septets = _unpack_septets(bytes.fromhex(compact), septet_count)
    return _decode_gsm7_septets(septets)


def encodeGsm7(message):
    return encode_gsm7(message)


def decodeGsm7(message, septet_count=None):
    return decode_gsm7(message, septet_count=septet_count)


def dec2hex(value):
    return hex(value).upper()[2:]


def hex2char(value):
    return chr(int(value, 16))


def _ensure_text(value, name):
    if not isinstance(value, str):
        raise TypeError("%s must be a string." % name)


def _normalize_hex_payload(value, chunk_size, label):
    _ensure_text(value, label)
    compact = "".join(value.split())

    if compact == "":
        return ""
    if len(compact) % chunk_size != 0:
        raise ValueError("%s must contain complete %s-hex chunks." % (label, chunk_size))
    if not _HEX_PATTERN.match(compact):
        raise ValueError("%s must contain only hexadecimal characters." % label)

    return compact.upper()


def _pack_septets(septets):
    packed = bytearray()
    buffer_value = 0
    bit_count = 0

    for septet in septets:
        buffer_value |= (septet & 0x7F) << bit_count
        bit_count += 7

        while bit_count >= 8:
            packed.append(buffer_value & 0xFF)
            buffer_value >>= 8
            bit_count -= 8

    if bit_count:
        packed.append(buffer_value & 0xFF)

    return bytes(packed)


def _unpack_septets(data, septet_count=None):
    if septet_count is not None:
        if not isinstance(septet_count, int):
            raise TypeError("septet_count must be an integer.")
        if septet_count < 0:
            raise ValueError("septet_count must be zero or greater.")

    septets = []
    buffer_value = 0
    bit_count = 0

    for octet in data:
        buffer_value |= octet << bit_count
        bit_count += 8

        while bit_count >= 7:
            septets.append(buffer_value & 0x7F)
            buffer_value >>= 7
            bit_count -= 7
            if septet_count is not None and len(septets) == septet_count:
                return septets

    if septet_count is not None and len(septets) != septet_count:
        raise ValueError("Packed GSM 7-bit payload does not contain %s septets." % septet_count)

    return septets


def _decode_gsm7_septets(septets):
    characters = []
    in_extension = False

    for septet in septets:
        if in_extension:
            if septet not in _GSM7_EXTENSION_DECODE_MAP:
                raise ValueError(
                    "Invalid GSM 7-bit extension code 0x%02X in packed payload." % septet
                )
            characters.append(_GSM7_EXTENSION_DECODE_MAP[septet])
            in_extension = False
            continue

        if septet == _GSM7_ESCAPE:
            in_extension = True
            continue

        if septet not in _GSM7_BASIC_DECODE_MAP:
            raise ValueError("Invalid GSM 7-bit code 0x%02X in packed payload." % septet)

        characters.append(_GSM7_BASIC_DECODE_MAP[septet])

    if in_extension:
        raise ValueError("Packed GSM 7-bit payload ends with a dangling escape code.")

    return "".join(characters)
