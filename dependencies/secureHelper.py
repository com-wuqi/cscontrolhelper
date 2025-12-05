from hashlib import sha256
from secrets import token_hex
from datetime import datetime, timedelta, timezone


def hash_salted_password(password: str) -> str:
    """
    计算加盐密码的SHA256哈希值

    Args:
        password: 原始密码字符串


    Returns:
        哈希值的十六进制字符串
    """
    return sha256(password.encode('utf-8')).hexdigest()

def generate_secret_key() -> str:
    return token_hex(256)

def generate_salt():
    return token_hex(64)