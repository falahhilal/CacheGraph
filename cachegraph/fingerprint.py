
import base64
import hashlib
import json
import math


def _normalize(value):
    if value is None:
        return ["none"]

    if type(value) is bool:
        return ["bool", value]

    if type(value) is int:
        return ["int", str(value)]

    if type(value) is float:
        if not math.isfinite(value):
            raise ValueError("Non-finite floats cannot be fingerprinted")

        return ["float", value.hex()]

    if type(value) is str:
        return ["str", value]

    if type(value) is bytes:
        encoded = base64.b64encode(value).decode("ascii")
        return ["bytes", encoded]

    if type(value) is list:
        return ["list", [_normalize(item) for item in value]]

    if type(value) is tuple:
        return ["tuple", [_normalize(item) for item in value]]

    if type(value) is dict:
        for key in value:
            if type(key) is not str:
                raise TypeError("Dictionary keys must be strings")

        normalized_items = []

        for key in sorted(value):
            normalized_items.append([key, _normalize(value[key])])

        return ["dict", normalized_items]

    raise TypeError(
        f"Unsupported type for fingerprinting: {type(value).__name__}"
    )


def fingerprint(value):
    normalized = _normalize(value)

    serialized = json.dumps(
        normalized,
        ensure_ascii=False,
        separators=(",", ":")
    ).encode("utf-8")

    return hashlib.sha256(serialized).hexdigest()
