
import hashlib


def get_hash_password(password: str):
    return hashlib.blake2b((f"sdfsdfe{password}e4dfc").encode("utf8"), digest_size=32).hexdigest()
