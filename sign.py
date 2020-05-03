import hashlib
import json
from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.Hash import SHA
from Cryptodome.PublicKey import RSA

class sign:

    def __init__(self):

        self.conf = json.load(open("conf.json"))
        self.private_key = self.conf['private_key']
        self.secret_code = self.conf['secret_code']

    def sign_message(self, message):

        response = hashlib.md5(message.encode('utf-8')).digest()
        key = RSA.import_key(open(self.private_key).read(), passphrase = self.secret_code)
        h = SHA256.new(response)
        signature = pkcs1_15.new(key).sign(h)

        return signature.hex()

    def verify_sign(self, message, sign, public_key):

        response = hashlib.md5(message.encode('utf-8')).digest()
        key = RSA.import_key(public_key)
        h = SHA256.new(response)
        try:
            pkcs1_15.new(key).verify(h, bytearray.fromhex(sign))
            return True
        except (ValueError, TypeError):
            return False



