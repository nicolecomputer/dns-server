NULL_BYTE = b"\x00"


def encode_label(label: str) -> bytes:
    encoded = label.encode("ascii")
    encoded_len = bytes([len(encoded)])

    return encoded_len + encoded
