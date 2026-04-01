import pytest

import pygsm7


@pytest.mark.parametrize(
    "message",
    [
        "Hello, world!",
        "Mambo na accents: éèñü",
        "control chars:\n\t\r\0done",
        "Emoji round trip: 😀🚀👨🏽\u200d💻",
    ],
)
def test_unicode_hex_round_trip(message):
    encoded = pygsm7.encode(message)

    assert encoded == pygsm7.encodeMessage(message)
    assert pygsm7.decode(encoded) == message
    assert pygsm7.decodeMessage(encoded) == message


def test_unicode_hex_decode_allows_whitespace_between_code_units():
    assert pygsm7.decode("0048 0065 006C 006C 006F") == "Hello"


def test_unicode_hex_round_trips_all_control_characters():
    message = "".join(chr(code) for code in list(range(0x20)) + [0x7F])

    assert pygsm7.decode(pygsm7.encode(message)) == message


@pytest.mark.parametrize("payload", ["123", "GGGG", "00", "D83D"])
def test_unicode_hex_decode_rejects_invalid_input(payload):
    with pytest.raises(ValueError):
        pygsm7.decode(payload)


def test_true_gsm7_round_trip_basic_text():
    message = "Hello GSM7"
    encoded = pygsm7.encode_gsm7(message)

    assert encoded == pygsm7.encodeGsm7(message)
    assert pygsm7.decode_gsm7(encoded) == message
    assert pygsm7.decodeGsm7(encoded) == message


def test_true_gsm7_round_trip_extension_characters():
    message = "^{}\\[~]|\f€"

    assert pygsm7.decode_gsm7(pygsm7.encode_gsm7(message)) == message


def test_true_gsm7_round_trips_full_supported_character_set():
    basic = "".join(
        chr(int(code, 16))
        for index, code in enumerate(pygsm7.GSM7_Table)
        if index != 0x1B
    )
    extension = "".join(chr(int(code, 16)) for code in pygsm7.GSM7_Table_Extend)
    message = basic + extension

    assert pygsm7.decode_gsm7(pygsm7.encode_gsm7(message)) == message


def test_true_gsm7_matches_known_packed_vector():
    assert pygsm7.encode_gsm7("hello") == "E8329BFD06"
    assert pygsm7.decode_gsm7("E8329BFD06") == "hello"


def test_true_gsm7_rejects_unsupported_characters():
    with pytest.raises(ValueError):
        pygsm7.encode_gsm7("No emoji 😀 in GSM7")


@pytest.mark.parametrize("payload", ["F", "ZZ", "1B"])
def test_true_gsm7_decode_rejects_invalid_input(payload):
    with pytest.raises(ValueError):
        pygsm7.decode_gsm7(payload)
