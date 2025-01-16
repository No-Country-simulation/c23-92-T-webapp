import secrets
import string

def generate_secret_key(length=32):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

if __name__ == "__main__":
    secret_key = generate_secret_key()
    refresh_secret_key = generate_secret_key(64)  # Puedes usar una longitud mayor para el refresh key
    
    print(f"Generated SECRET_KEY: {secret_key}")
    print(f"Generated REFRESH_SECRET_KEY: {refresh_secret_key}")
