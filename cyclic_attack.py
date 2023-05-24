import sys
import secrets
import math
import time

def generate_rsa_prime_numbers(x):
    while True:
        p = secrets.randbits(x) | (1 << (x-1)) | 1  # Generate a random odd number of x bits
        while not is_prime(p):
            p += 2  # Increment by 2 to maintain oddness

        q = secrets.randbits(x) | (1 << (x-1)) | 1  # Generate another random odd number of x bits
        while not is_prime(q) or q == p:
            q += 2  # Increment by 2 to maintain oddness

        if p != q:
            return p, q

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    for i in range(5, math.isqrt(n) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True

def modular_exponentiation(base, exponent, modulus):
    result = 1

    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent //= 2

    return result

def cyclic_attack(ciphertext, n, f4number):
    attempts = 0
    while True:
        last_ciphertext = ciphertext
        ciphertext = modular_exponentiation(last_ciphertext, f4number, n)
        current_time = time.time()
        elapsed_time = current_time - start_time
        attempts_per_second = attempts / elapsed_time
        sys.stdout.write("\r")
        sys.stdout.write(f"Elapsed Time: {elapsed_time:.2f}s | Attemps: {attempts} | Attempts/s: {attempts_per_second:.2f} | Cipher Text: {ciphertext}")
        
        if ciphertext == original_ciphertext:
            sys.stdout.write("\r")
            sys.stdout.write(f"\nOriginal message found: {last_ciphertext}")
            return last_ciphertext
        attempts = attempts + 1
        sys.stdout.flush()


sys.stdout.write(f"\n-- Cyclic Attack on RSA by Pablo Osés --\n")

prime_number_bits = 19
# Public key (n, f4number)
p, q = generate_rsa_prime_numbers(prime_number_bits)
n = p * q
f4number = 65537

# Ciphertext
message = 13245
original_ciphertext = modular_exponentiation(message, f4number, n)

# Begin cyclic attack
sys.stdout.write(f"Starting RSA cyclic attack:\nPublic Key:({n},{f4number}) n-bits:{prime_number_bits*2}\nCypher text: {original_ciphertext}\n\n")
start_time = time.time()
cyclic_attack_result = cyclic_attack(original_ciphertext, n, f4number)
end_time = time.time()
sys.stdout.write(f"\nHappy hacking! ^.^\n\n")
