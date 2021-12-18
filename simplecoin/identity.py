import rsa


from typing import Tuple

RSA_KEY_SIZE = 512
RSA_HASH_METHOD = 'SHA-256'


def sign(message: str, private_key: rsa.PrivateKey) -> bytes:
    return rsa.sign(bytes(message, encoding='utf8'), private_key, RSA_HASH_METHOD)


def is_key_signature(message: str, signature: bytes, public_key: rsa.PublicKey) -> bool:
    try:
        if rsa.verify(bytes(message, encoding='utf8'), signature, public_key) == RSA_HASH_METHOD:
            return True
    except rsa.VerificationError:
        return False

    return False


def newkeys() -> Tuple[rsa.PublicKey, rsa.PrivateKey]:
    return rsa.newkeys(RSA_KEY_SIZE)

