#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 dutoe <dutoe@wyl-node>
#
# Distributed under terms of the MIT license.

"""

"""

import rsa_crypt
from base64 import b64encode, b64decode

msg1 = "Hello Tony, I am Jarvis!"
msg2 = "Hello Toni, I am Jarvis!"
keysize = 2048
(public, private) = rsa_crypt.newkeys(keysize)
encrypted = b64encode(rsa_crypt.encrypt(msg1, public))
decrypted = rsa_crypt.decrypt(b64decode(encrypted), private)
signature = b64encode(rsa_crypt.sign(msg1, private, "SHA-512"))
verify = rsa_crypt.verify(msg1, b64decode(signature), public)

print(private.exportKey('PEM'))
print(public.exportKey('PEM'))
print("Encrypted: " + encrypted)
print("Decrypted: '%s'" % decrypted)
print("Signature: " + signature)
print("Verify: %s" % verify)
rsa_crypt.verify(msg2, b64decode(signature), public)
