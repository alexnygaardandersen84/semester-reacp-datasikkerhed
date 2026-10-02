import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    return password_hash.decode("utf-8")
    
def verify_password(password: str, stored_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        stored_hash.encode("utf-8"),
    )


print(hash_password("Test"))