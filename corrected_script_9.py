import hashlib
import random
import os
#import secrets # needs python 3.6

OTPNUM = 50
ALGORITHM = 'sha1'

#key = secrets.token_bytes(2048) # needs python 3.6
key = os.urandom(256)

lastkey = hashlib.new(ALGORITHM, key).hexdigest()

otps = []

for i in range(OTPNUM):
    lastkey = hashlib.new(ALGORITHM, lastkey.encode()).hexdigest()
    otps.append(lastkey)

for i, otp in enumerate(reversed(otps)):
    print('{:>4} {}'.format(i, otp))

while True:
    while True:
        response = input('Enter the hash that follows ' + lastkey + ': ')
        result = hashlib.new(ALGORITHM, response.encode()).hexdigest()
        if result == lastkey:
            print('OK!')
            lastkey = response
            break
        else:
            print('Error. Try again')