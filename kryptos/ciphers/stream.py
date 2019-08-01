import numpy as np
import itertools
from collections import defaultdict
import operator
import string
import binascii

class StreamCipherSolver():
    def __init__(self):
        self.ciphertexts = []
        self.get_file_input()
        #self.get_input()
        self.ciphertext_chunks = [list(bytearray.fromhex(cipher)) for cipher in self.ciphertexts]
        self.key = ['00'] * max(map(len, self.ciphertext_chunks))

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
        estimated_key = []
        for i in range(len(self.key)):
            # check the ith byte of every array, if applicable
            possible_keys = defaultdict(lambda: ('0x00', -1))
            score = defaultdict(int)
            for idx in np.ndindex(self.xor_products.shape[:2]):
                curr_list = self.xor_products[idx]
                # print(len(curr_list), list(len(self.ciphertext_chunks[j]) for j in idx), i)
                if len(curr_list) > i and min([len(self.ciphertext_chunks[j]) for j in idx]) > i:
                    if curr_list[i].isalpha(): # if ith byte is alpha, then that byte likely encodes a space 
                        test_bytes = [self.ciphertext_chunks[ii][i] for ii in idx]
                        # we come up with n possible keys given that one of the ciphertexts encodes a space
                        candidate_keys = [byte ^ ord(' ') for byte in test_bytes]
                        
                        # test each of the n possible keys on a "validation set" of ciphertext bytes - the ith byte of all other ciphertexts
                        validation_cipher_indices = [ii for ii in range(len(self.ciphertext_chunks)) if ii not in idx] # 
                        validation_bytes = [self.ciphertext_chunks[ii][i] for ii in validation_cipher_indices if i < len(self.ciphertext_chunks[ii])]
                        for candidate, validator in itertools.product(candidate_keys, validation_bytes):
                            character = chr(candidate ^ validator)
                            alpha_pred = int(character.isalpha())
                            num_pred = int(character.isdigit())
                            punct_pred = int(character in string.punctuation)
                            score[hex(candidate)] += 5 * alpha_pred + num_pred # if xoring the candidate key with the validation byte yields an alphanumeric character, this is good
                        best_key = max(score.items(), key=operator.itemgetter(1), default=('0x00', -1)) # find which key has the most "hits"
                        if best_key[1] > possible_keys[i][1]:
                            possible_keys[i] = best_key
            # print("{0}:".format(i), possible_keys[i])
            estimated_key.append(possible_keys[i][0])
        self.key = estimated_key
        return estimated_key

    def mle_decrypt(self, ciphertext, key):
        # print(ciphertext, key)
        result = []
        key_arr = [int(key_byte, 16) for key_byte in key][:len(ciphertext)]
        for byte1, byte2 in zip(ciphertext, key_arr):
            result.append(chr(byte1 ^ byte2))
        return ''.join(result)

    def key_substitute(self, cipher_idx, position, plainchar):
        key_copy = [k for k in self.key]
        key_copy[position] = hex(self.ciphertext_chunks[cipher_idx][position] ^ ord(plainchar))
        return key_copy

    def encode_with_key(self, message):
        hex_msg = list(bytearray("hello".encode('ascii')))
        result = []
        for byte1, byte2 in zip(hex_msg, itertools.cycle(key_arr)):
            result.append(hex(byte1 ^ int(byte2, 16)))
        return ''.join(map(operator.itemgetter(slice(2, None)), result))
    
if __name__ == '__main__':
    solver = StreamCipherSolver()
    solver.xor_product()
    key_arr = solver.analyze()
    for i in range(len(solver.ciphertext_chunks)):
        print("Msg {0}:".format(i), solver.mle_decrypt(solver.ciphertext_chunks[i], key_arr))

