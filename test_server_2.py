import BaseHTTPServer
import urlparse
from Crypto.Cipher import AES

class Server(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        parsed_qs = urlparse.parse_qs(parsed_path.query)
        if parsed_path.path == "/checkcreds":
            enc = parsed_qs["enc"][0]
            try:
                if self.checkcreds(enc):
                    self.send_response(200)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write("A 200 page")
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/plain")
                    self.end_headers()
                    self.wfile.write("A 404 page")
            except Exception, e:
                self.send_response(500)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write("Exception")
                self.wfile.write(e)
                return

    def checkcreds(self, enc):
        key = "a" * 16
        message = CryptoHelper.decrypt(enc.decode("hex"), key)
        if message != "b":
            print "Invalid message is ", repr(message)
            return False
        return True

class CryptoHelper:
    IV = "LOLOLOLOLOLOLOLO"

    @staticmethod
    def encrypt(message, key):
        message = CryptoHelper.padPKCS7(message)
        aes = AES.new(key, AES.MODE_CBC, CryptoHelper.IV)
        ciphertext = aes.encrypt(message)
        return ciphertext

    @staticmethod
    def padPKCS7(message):
        length = 16 - (len(message) % 16)
        message += chr(length)*length
        return message

    @staticmethod
    def decrypt(ciphertext, key):
        aes = AES.new(key, AES.MODE_CBC, CryptoHelper.IV)
        message = aes.decrypt(ciphertext)
        print ">>>", repr(message)
        message = CryptoHelper.unpadPKCS7(message)
        return message

    @staticmethod
    def unpadPKCS7(message):
        if len(message)%16 or not message:
            raise ValueError("Invalid message len")
        padlen = ord(message[-1])
        if padlen > 16:
            raise ValueError("Invalid padding")
        if padlen == 0:
            raise ValueError("Invalid padding")
        for i in range(padlen):
            if ord(message[-(i + 1)]) != padlen:
                raise ValueError("Invalid padding")
        return message[:-padlen]


def main():
    cipher = CryptoHelper.encrypt("b"*16, "a"*16)
    print cipher.encode("hex")
    httpd = BaseHTTPServer.HTTPServer(("localhost", 80), Server)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt, e:
        pass
    httpd.server_close()


if __name__ == '__main__':
    main()
