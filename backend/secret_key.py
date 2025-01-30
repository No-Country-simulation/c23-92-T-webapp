import base64
import secrets
import string

def generate_secret_key(length=32):
    safe_characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{};:,.<>?"
    return ''.join(secrets.choice(safe_characters) for _ in range(length))

def generate_binary_key(length=32):
    key = secrets.token_bytes(length)
    return base64.urlsafe_b64encode(key).decode('utf-8')

if __name__ == "__main__":
    secret_key = generate_secret_key()
    refresh_secret_key = generate_secret_key(64)
    refresh_encryption_key = generate_binary_key(32)
    cookie_secret_key = generate_binary_key(32)

    print(f"Generated SECRET_KEY: {secret_key}")
    print(f"Generated REFRESH_SECRET_KEY: {refresh_secret_key}")
    print(f"Generated REFRESH_ENCRYPTION_KEY: {refresh_encryption_key}")
    print(f"Generated COOKIE_SECRET_KEY: {cookie_secret_key}")