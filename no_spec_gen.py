import string
import secrets

gen_base = string.ascii_letters + string.digits

def no_spec_gen(length: int = 20) -> str:
    """Generate a password with at least one lower, one upper, and >=4 digits.
    Minimum length is 6 (1 lower + 1 upper + 4 digits = 6)."""
    min_len = 6
    if length < min_len:
        raise ValueError(f"no_spec_gen requires length >= {min_len}")
    while True:
        password = ''.join(secrets.choice(gen_base) for _ in range(length))
        if (any(x.islower() for x in password) and
            any(x.isupper() for x in password) and
            sum(x.isdigit() for x in password) >= 4):
            return password
