import os
import argon2

# Generate a random salt using a CSPRNG
def generate_salt(salt_len):
    salt = os.urandom(salt_len).hex()
    return salt

# Generate a random salt using a CSPRNG
def generate_pepper(pepper_len):
    pepper = os.urandom(pepper_len).hex()
    return pepper

# Hashing function using Argon2 with salt and pepper
def hash_password(password, salt, pepper):
    # Combine the password and pepper
    password += salt
    password += pepper

    # Hash the password using Argon2 with a random salt
    hasher = argon2.PasswordHasher(
        hash_len = 80,
        salt_len = 32,
        time_cost = 10,
        memory_cost = 2**12,
        parallelism = 6,
        encoding='ascii'
        )
    hashed_password = hasher.hash(password)
    return hashed_password

# Verification function for hashed passwords
def verify_password(hashed_password, password, salt, pepper):
    salt = str(salt)
    pepper = str(pepper)

    # Combine the password and pepper
    password += salt
    password += pepper

    # Verify the password against its hashed version using Argon2
    hasher = argon2.PasswordHasher(
        hash_len = 80,
        salt_len = 32,
        time_cost = 10,
        memory_cost = 2**12,
        parallelism = 6,
        encoding='ascii'
        )
    
    try:
        hasher.verify(hashed_password, password)
        return True
    except argon2.exceptions.VerificationError:
        return False
    except argon2.exceptions.InvalidHash:
        return False


"""# Generate random salt and pepper using os.urandom
salt = os.urandom(32).hex()
pepper = os.urandom(32).hex()

# Example usage
password1 = "my_password1"
password2 = "my_password1"
hashed_password = hash_password(password1, salt, pepper)

print(f"Salt: {salt}")
print(f"Pepper: {pepper}")
print(f"Hashed Password: {hashed_password}")

if verify_password(hashed_password, password2, salt, pepper):
    print("Password is correct!")
else:
    print("Password is incorrect.")
"""