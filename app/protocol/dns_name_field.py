from dataclasses import dataclass
from app.protocol.util import encode_label, NULL_BYTE


@dataclass
class DNSNameField:
    name: str

    def to_bytes(self) -> bytes:
        if not self.name:
            return NULL_BYTE

        labels = self.name.split(".")
        encoded_labels = [encode_label(label) for label in labels]

        return b"".join(encoded_labels) + NULL_BYTE
