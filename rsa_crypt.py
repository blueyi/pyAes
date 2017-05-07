#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 dutoe <dutoe@wyl-node>
#
# Distributed under terms of the MIT license.

"""

"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA512, SHA384, SHA256, SHA, MD5
from Crypto import Random
from base64 import b64encode, b64decode

hash = "SHA-256"

def newkeys(keysize):
    random_generator = Random.new().read
    key = RSA.generate(keysize, random_generator)
    private, public = key, key.publickey()
    return public, private

def importKey(externKey):
    return RSA.importKey(externKey)

def getpublickey(priv_key):
    return priv_key.publickey()

def encrypt(message, pub_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(pub_key)
    return cipher.encrypt(message)

def decrypt(ciphertext, priv_key):
    #RSA encryption protocol according to PKCS#1 OAEP
    cipher = PKCS1_OAEP.new(priv_key)
    return cipher.decrypt(ciphertext)

def sign(message, priv_key, hashAlg="SHA-256"):
    global hash
    hash = hashAlg
    signer = PKCS1_v1_5.new(priv_key)
    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.sign(digest)

def verify(message, signature, pub_key):
    signer = PKCS1_v1_5.new(pub_key)
    if (hash == "SHA-512"):
        digest = SHA512.new()
    elif (hash == "SHA-384"):
        digest = SHA384.new()
    elif (hash == "SHA-256"):
        digest = SHA256.new()
    elif (hash == "SHA-1"):
        digest = SHA.new()
    else:
        digest = MD5.new()
    digest.update(message)
    return signer.verify(digest, signature)

# write msg to file
def to_file(filename, msg):
    with open(filename, 'w') as f:
        f.write(msg)

# read string from file
def from_file(filename):
    with open(filename, 'r') as f:
        return f.read()

# generate new rsa key and write to file pri.pem and pub.pem
def gen_new_rsa_to_file(key_size):
    (public, private) = newkeys(key_size)
    to_file('pri.pem', private.exportKey('PEM'))
    to_file('pub.pem', public.exportKey('PEM'))

# gen_new_rsa_to_file(2048)

# encode msg by public pem key file, then return the encode string
def enc_from_pubfile(msg, pub_file):
    pub_key = importKey(from_file(pub_file))
    return b64encode(encrypt(msg, pub_key))

# decode base64 encode msg by private pem key file, then return the original string
def dec_from_prifile(base64_enc_msg, pri_file):
    pri_key = importKey(from_file(pri_file))
    return decrypt(b64decode(base64_enc_msg), pri_key)


# encode file's content line by line, then write line by line to new file
def enc_file_to_file(ori_file, pub_file, enc_file):
    enc_list = []
    pub_key = importKey(from_file(pub_file))
    for line in open(ori_file, 'r'):
        enc_list.append(b64encode(encrypt(line.strip(), pub_key)))
    newFile = open(enc_file, 'w')
    newFile.write("\n".join(enc_list))
    return enc_list


# decode file's content line by line, then write line by line to new file, return decode list
def dec_file_to_file(enc_file, pri_file, dec_file=None):
    dec_list = []
    pri_key = importKey(from_file(pri_file))
    for line in open(enc_file, 'r'):
        dec_list.append(decrypt(b64decode(line.strip()), pri_key))
    newFile = open(dec_file, 'w')
    newFile.write("\n".join(dec_list))
    return dec_list