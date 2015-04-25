import urllib
import logging
import sys

from oracle import PaddingAttack

import Colorer

sample_encrypted = "e72542db2eefcb6cf59cf6abf78979f91c9f0143c22a959eb5c59cd55b366d713f3a2f5614bcee12d372137dbd58629febf307b291aab18d88b5ca63727d10b2"

def try_sending(enc_block):
    base_url = "http://localhost:7171/checkcreds?enc="
    base_url += enc_block
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
    logger = logging.getLogger("test_oracle_basic")

    p = PaddingAttack(sample_encrypted[0:32], "LOLOLOLOLOLOLOLO".encode("hex"), try_sending, 16)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[32:64], sample_encrypted[0:32], try_sending, 16)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[64:96], sample_encrypted[32:64], try_sending, 16)
    logger.info(p.attack())
    p = PaddingAttack(sample_encrypted[96:128], sample_encrypted[64:96], try_sending, 16)
    logger.info(p.attack())

if __name__ == '__main__':
    main()

