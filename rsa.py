import random
from math import floor
from math import sqrt

RANDOM_START = int(1e3)
RANDOM_END = int(1e5)

def is_prime(num):
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, floor(sqrt(num))):
        if num % i == 0:
            return False
    return True

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def modular_inverse(a, b):
    if a == 0:
        return b, 0, 1
    div, x1, y1 = modular_inverse(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return div, x, y

def generate_large_prime(start=RANDOM_START, end=RANDOM_END):
    num = random.randint(start, end)
    while not is_prime(num):
        num = random.randint(start, end)
    return num

def generate_rsa_keys():
    p = generate_large_prime()
    q = generate_large_prime()
    n = p * q
    phi = (p-1)*(q-1)
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    d = modular_inverse(e, phi)[1]

    return (d, n), (e, n)

def encrypt(public_key, plain_text):
    e, n = public_key

    cipher_text = []

    for char in plain_text:
        a = ord(char)
        cipher_text.append(pow(a, e, n))

    return cipher_text

def decrypt(private_key, cipher_text):
    d, n = private_key
    plain_text = ''
    for num in cipher_text:
        a = pow(num, d, n)
        plain_text = plain_text + str(chr(a))
    return plain_text


if __name__ == '__main__':
    private_key, public_key = generate_rsa_keys()
    message = 'This is an example message with RSA algorithm!'
    print("Original message: %s" % message)
    cipher = encrypt(public_key, message)
    print("Cipher text: %s" % cipher)
    plain = decrypt(private_key, cipher)
    print("Decrypted text: %s" % plain)