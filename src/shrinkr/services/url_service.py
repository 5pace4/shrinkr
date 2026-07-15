import hashlib


BASE62_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def base62_encode(number: int) -> str:
    """Convert a positive integer into a Base62 string."""
    if number == 0:
        return BASE62_ALPHABET[0]

    encoded_chars = []
    while number > 0:
        number, remainder = divmod(number, 62)
        encoded_chars.append(BASE62_ALPHABET[remainder])

    return "".join(reversed(encoded_chars))


def make_shortend_url(original_url: str) -> str:
    """Generate a deterministic short code using MD5 hashing and Base62 encoding."""
    md5_digest = hashlib.md5(original_url.encode()).digest()
    short_seed = int.from_bytes(md5_digest[:6], byteorder="big")
    return base62_encode(short_seed)