import secrets

# Generate a 32-byte (256-bit) secure key
secure_key = secrets.token_urlsafe(32)
print(secure_key)