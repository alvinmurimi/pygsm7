try:
    from .pygsm7 import decode, decodeMessage, encode, encodeMessage
except ImportError:
    from pygsm7 import decode, decodeMessage, encode, encodeMessage

__all__ = ["encode", "decode", "encodeMessage", "decodeMessage"]
