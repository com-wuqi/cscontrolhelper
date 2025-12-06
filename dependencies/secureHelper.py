from hashlib import sha256
from secrets import token_hex


def hash_salted_password(password: str) -> str:
    return sha256(password.encode('utf-8')).hexdigest()

def generate_secret_key() -> str:
    return token_hex(64)

# def generate_salt():
#     return token_hex(64)