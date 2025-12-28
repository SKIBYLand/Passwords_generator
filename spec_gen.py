import string
import secrets

spec_gen_base = string.ascii_letters + string.digits + string.punctuation

def spec_gen(length: int = 20) -> str:
    """Generate a password with at least one lower, one upper, >=4 digits, and at least one punctuation.
    Minimum length is 7 (1 lower + 1 upper + 4 digits + 1 punctuation = 7)."""
    min_len = 7
    if length < min_len:
        raise ValueError(f"spec_gen requires length >= {min_len}")
    while True:
        password = ''.join(secrets.choice(spec_gen_base) for _ in range(length))
        if (any(x.islower() for x in password) and
            any(x.isupper() for x in password) and
            sum(x.isdigit() for x in password) >= 4 and
            any(x in string.punctuation for x in password)):
            return password
