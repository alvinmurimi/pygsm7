try:
    from .pygsm7 import (
        decode,
        decode_gsm7,
        decodeGsm7,
        decodeMessage,
        encode,
        encode_gsm7,
        encodeGsm7,
        encodeMessage,
    )
except ImportError:
    from pygsm7 import (
        decode,
        decode_gsm7,
        decodeGsm7,
        decodeMessage,
        encode,
        encode_gsm7,
        encodeGsm7,
        encodeMessage,
    )

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
