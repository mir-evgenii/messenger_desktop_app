from Cryptodome.Signature import pkcs1_15
from Cryptodome.Hash import SHA256
from Cryptodome.Hash import SHA
from Cryptodome.PublicKey import RSA

class sign:

    def __init__(self):

        self.private_key = 'bob_private_rsa_key_pass.pem'
        self.secret_code = 'qwe123'

    def sign_message(self, message):

        response = bytes(message, encoding = 'utf-8')
        key = RSA.import_key(open(self.private_key).read(), passphrase = self.secret_code)
        h = SHA256.new(response)
        signature = pkcs1_15.new(key).sign(h)

        return signature.hex()

    def verify_sign(self, message, sign, public_key):

        response = bytes(message, encoding = 'utf-8')
        key = RSA.import_key(public_key)
        h = SHA256.new(response)
        try:
            pkcs1_15.new(key).verify(h, bytearray.fromhex(sign))
            return True
        except (ValueError, TypeError):
            return False



