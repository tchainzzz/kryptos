import numpy as np
import itertools

class StreamCipherSolver():
    def __init__(self):
        self.ciphertexts = []
        self.get_file_input()
        #self.get_input()
        self.key = ['00'] * max(map(len, self.ciphertexts))
        self.ciphertext_chunks = [list(bytearray.fromhex(cipher_hex)) for cipher in self.ciphertexts]

    def get_file_input(self):
        with open("code") as f:
            self.ciphertexts = list(f)

    def get_input(self):
        while True:
            cipher = input("Cipher #{0}: ".format(len(self.ciphertexts) + 1))
            if not len(cipher):
                break
            self.ciphertexts.append(cipher)

    def xor_product(self):
       self.xor_products = np.empty((len(self.ciphertexts), len(self.ciphertexts)), dtype=list)
       for (index1, cipher1), (index2, cipher2) in itertools.product(enumerate(self.ciphertexts), enumerate(self.ciphertexts)):
           if len(cipher1) > len(cipher2):
               cipher1 = cipher1[:len(cipher2)]
           if len(cipher2) > len(cipher1):
               cipher2 = cipher2[:len(cipher1)]
           cipher_hex = hex(int(cipher1, 16) ^ int(cipher2, 16))[2:]
           if len(cipher_hex) % 2 == 1:
               cipher_hex = "0" + cipher_hex
           self.xor_products[index1, index2] = [chr(i) for i in list(bytearray.fromhex(cipher_hex))]

    def analyze(self):
        for i in range(len(self.key)):


if __name__ == '__main__':
    solver = StreamCipherSolver()
    solver.xor_product()

