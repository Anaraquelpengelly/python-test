import re
import tempfile
import os

sample_passwords = [
    "Password123!",
    "AnotherGoodPassword456",
    "P@ssw0rd12345",
    "ThisIsALongPasswordWithNumbers123AndSymbols!@#",
    "short",
    "NoDigitsNoUpper",
    "no_lower_1234",
    "ONLYUPPERCASEANDNUMBERS123",
    "123456789012",
    "abcdefghijkl",
    "ABCDEFGHIJKL",
    "Pass1234567890",
    "Short123",
]

with tempfile.NamedTemporaryFile(mode='w', delete=False, prefix='darkweb2017-top10000', suffix='.txt') as tmp:
    tmp_path = tmp.name
    for p in sample_passwords:
        tmp.write(p + '\n')
    tmp.flush()

try:
    with open(tmp_path, 'r') as f:
        for password in f.readlines():

            password = password.strip()

            if len(password) < 12:
                continue

            if len(re.findall(r'[a-z]', password)) < 1:
                continue

            if len(re.findall(r'[A-Z]', password)) < 1:
                continue

            if len(re.findall(r'[0-9]', password)) < 1:
                continue

            print(password)
finally:
    if os.path.exists(tmp_path):
        os.unlink(tmp_path)