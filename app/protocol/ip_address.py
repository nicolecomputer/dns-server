from typing import Tuple

class IPAddress:
    value: Tuple[int, int, int, int]
    length: int = 4

    def __init__(self, a: int, b: int, c: int, d: int):
        self.value = (a, b, c, d)
        self.length = 4

    def encode(self) -> bytes:
        return self.value[0].to_bytes(1, byteorder="big") + \
            self.value[1].to_bytes(1, byteorder="big") + \
            self.value[2].to_bytes(1, byteorder="big") + \
            self.value[3].to_bytes(1, byteorder="big")
