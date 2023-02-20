import secrets
import string

def make_access_token(n=16):
    chars = string.ascii_letters + string.digits
    return ''.join([secrets.choice(chars) for _ in range(n)])