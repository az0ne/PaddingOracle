This is (yet another) Python library that tries to ease padding attack exploitation.

PaddingOracle
============

An example of how you could use [oracle](https://github.com/eQu1NoX/PaddingOracle/blob/master/oracle.py) can be found [here](https://github.com/eQu1NoX/PaddingOracle/blob/master/test_oracle_basic.py).

In order to use `PaddingAttack` you'd have to create an instance of the class using the following mandatory arguments:

* The `ciphertext`
* The `IV`
* A function object `callback`

Optional arguments are :

* `blocksize`, defaults to 16 bytes
* debug `lvl`, defaults to INFO

A few words on the callback function
------------------------------------
The callback function is used to abstract away how the exploitation is to be done from the actual mechanism(which is pretty much the same always). The callback function accepts as an argument a crafted hex-encoded ciphertext. The callback function is responsible for :-

* accepting a crafted ciphertext `enc_block`
* sending `enc_block` over to the server(via cookies, POST, GET, whatever)
* gauging the response: If the decryption was successful and resulted in a valid message, return a `200` to the caller. If the decryption was sucessful(but did not result in a valid message) return a `404`. If an invalid padding exception was raised at the server side, return a `500`.

An example that uses `PaddingAttack` can be found [here](https://github.com/eQu1NoX/PaddingOracle/blob/master/test_oracle_aes_128.py).

Note
----
The PaddingOracle API deals with bytes. No input to the API should be in
encoded form. Similarly, the ciphertext that is passed as an argument to
the callback function will not be encoded. It is upto the user to use
the appropriate encoding/decoding mechanism.

Watching PaddingOracle in action
--------------------------------
Not very exciting to watch, you've been warned. ;-)

However if you must, clone the repo, run `python test_server.py` and
`python test_oracle_basic.py`

