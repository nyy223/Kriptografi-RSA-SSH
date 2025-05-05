# Kriptografi-RSA-SSH

### Nayla Raissa Azzahra / 5027231054
Pembelajaran dan praktik hands-on ini mengambil referensi dari https://github.com/mocatfrio/cryptography-2025/blob/master/RSA-SSH.md 

## RSA Encryption Hands-on (Python)
Proyek ini merupakan implementasi sederhana dari algoritma RSA (Rivest–Shamir–Adleman), sebuah algoritma kriptografi kunci publik yang digunakan untuk mengamankan data melalui proses enkripsi dan dekripsi.

#### Tujuan Hands-on
- Memahami bagaimana RSA bekerja: mulai dari generate key, enkripsi, hingga dekripsi.
- Mempelajari konsep bilangan prima, GCD, dan modular inverse.
- Melakukan praktik langsung dengan bahasa Python.

#### Konsep RSA secara Singkat
1. Generate dua bilangan prima secara acak: `p` dan `q`.
2. Hitung nilai `n = p * q` dan `phi = (p-1)*(q-1)`.
3. Pilih `e` sebagai eksponen publik (relatif prima terhadap `phi`).
4. Hitung `d` sebagai invers dari `e` terhadap `phi` menggunakan Extended Euclidean Algorithm.
5. Public key = `(e, n)`
6. Private key = `(d, n)`
7. Enkripsi: `cipher = (ord(char)^e) % n`
8. Dekripsi: `plain = (cipher^d) % n`

#### Langkah-langkah
script rsa.py
```bash
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
```
Jalankan script 
`python rsa.py`

Ouput yang akan dihasilkan
<img width="952" alt="Screenshot 2025-05-05 at 16 35 12" src="https://github.com/user-attachments/assets/226177e3-7660-4291-b2e6-be8167fbd597" />

## SSH Server Hands-On (Docker)
Pada bagian ini, kita akan mempraktikkan bagaimana membuat dan menjalankan server SSH menggunakan Docker container. Praktik ini bertujuan untuk memahami bagaimana protokol SSH bekerja serta bagaimana kita bisa mengakses server menggunakan SSH key secara lebih aman.

#### Tujuan Hands-On
1. Menjalankan SSH server di dalam container Docker.
2. Mengakses container menggunakan SSH client melalui public-private key.
3. Memahami bagaimana proses autentikasi SSH key-based bekerja secara praktikal.

#### Langkah-langkah
1. Buat folder proyek
```bash
mkdir ssh-server-docker
cd ssh-server-docker
```
2. Buat file bernama Dockerfile
```bash
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && \
    apt install -y openssh-server sudo && \
    mkdir /var/run/sshd

RUN useradd -ms /bin/bash student && \
    echo "student:student" | chpasswd && \
    echo "student ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

RUN mkdir /home/student/.ssh && \
    chmod 700 /home/student/.ssh && \
    chown student:student /home/student/.ssh

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
```
3. Build image Docker
```bash
docker build -t ssh-server .
```
4. Jalankan container
```bash
docker run -d --name ssh-demo -p 2222:22 ssh-server
```
5. Generate SSH key
```bash
ssh-keygen -t rsa -b 2048 -C "student@localhost"
```
<img width="609" alt="Screenshot 2025-05-05 at 16 47 18" src="https://github.com/user-attachments/assets/5a63ce92-f7e8-4a2e-96b8-c0f23ac6dc47" />

6. Copy public key ke container
```bash
docker exec -i ssh-demo bash -c 'cat >> /home/student/.ssh/authorized_keys' < ~/.ssh/id_rsa.pub
docker exec ssh-demo chown student:student /home/student/.ssh/authorized_keys
docker exec ssh-demo chmod 600 /home/student/.ssh/authorized_keys
```
7. Uji login
```bash
ssh -p 2222 student@localhost
```
<img width="612" alt="Screenshot 2025-05-05 at 16 47 43" src="https://github.com/user-attachments/assets/05378174-dad8-4369-b9d9-b66c740c889e" />

Terbukti dapat login tanpa menggunakan password
