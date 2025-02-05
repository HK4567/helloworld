#!/bin/python

import random
import requests,json
import time
import uuid
import secrets
import re
import rsa
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import md5
import wget
import base64
import os


sitekey = "9464902a3345d323ed58bde565f260ee"

t = {
    'height': 200.35000610351562,
    'width': 300.375
}

def guid():
    e = []
    for _ in range(4):
        e.append(secrets.token_hex(2))
    return ''.join(e)

def first_response(sitekey):
    response = requests.get(
         "https://gcaptcha4.geetest.com/load",
         params={
            "captcha_id": sitekey,
            "challenge": uuid.uuid4(),
            "client_type": "web_mobile",
            "lang": "zh-cn"
         })
    return response.text

def get_agrs(x):
    r = first_response(sitekey)
    r = json.loads(re.findall(r"\((.*)\)", r)[0])
    ques = r['data']['ques']
    ques.append(r['data']['imgs'])
    if x:
        return [ques,r['data']['lot_number'],r['data']['payload'],r['data']['process_token'],r['data']['pow_detail']['datetime']]
 
r_list = get_agrs(1)

def map_recognition():  
    image_base = []
    for _ in r_list[0]:
        image_url = "https://static.geetest.com/" + _
        wget.download(image_url,image_url.split("/")[-1])
        with open("%s" %(image_url.split("/")[-1]),"rb") as f:
            s = f.read()
            s = base64.b64encode(s).decode("ascii")
        image_base.append(s)
        time.sleep(1)
        os.remove(_.split("/")[-1])
    _url = "https://api.jfbym.com/api/YmServer/customApi"
    _data = {
            'token': 'GVy_zUhURyS3hwwDD0sWVF0DNEg6_cCvXh5EbbuHnUc',
            'type': '31111',
            'image': image_base[3],
            'image_label1': image_base[0],
            'image_label2': image_base[1],
            'image_label3': image_base[2],
            'extra': 'je4_click'
            }
    _headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", _url, headers=_headers, json=_data)
    return response.json()["data"]["data"]

def get_coordinate(x,y):
    x = (int(x) / t['width']) * 100
    y = (int(y) / t['height']) *100
    x = round(x * 100)
    y = round(y * 100)
    return [x,y]

def get_userresponse(z):
    userresponse = []
    c = z.split("|")
    for _ in c:
        _ = _.split(",")
        userresponse.append(get_coordinate(_[0],_[1]))
    print('userrsponse:',userresponse,'\n')
    return userresponse

guid = guid()

def get_pow_msg():
    return f"1|0|md5|{r_list[4]}|{sitekey}|{r_list[1]}||{guid}"

data = {
        "passtime": random.randint(19000, 38999),
        "userresponse": get_userresponse(map_recognition()),
        "device_id": "",
        "lot_number": r_list[1],
        "pow_msg": get_pow_msg(),
        "pow_sign": md5(get_pow_msg().encode()).hexdigest(),
        "gee_guard": None,
        "geetest": "captcha",
        "lang": "zh",
        "ep": "123",
        "em": {"cp": "0","ek": "11","nt": "0","ph": "0","sc": "0","si": "0","wd": "1"},
        "18Ri": "MYHo",
        "97fb4e": "0c2eb7",
        "biht": "1426265548"
    }
print('====================================================\n')
def encryp(data,guid):    
    e = int("10001", 16)
    n = int("00C1E3934D1614465B33053E7F48EE4EC87B14B95EF88947713D25EECBFF7E74C7977D02DC1D9451F79DD5D1C10C29ACB6A9B4D6FB7D0A0279B6719E1772565F09AF627715919221AEF91899CAE08C0D686D748B20A3603BE2318CA6BC2B59706592A9219D0BF05C9F65023A21D2330807252AE0066D59CEEFA5F2748EA80BAB81".lower(), 16)
    encryptor = AES.new(guid.encode('utf-8'), AES.MODE_CBC, iv=b"0000000000000000")
    pad_pkcs7 = pad(data.encode('utf-8'), AES.block_size, style='pkcs7')
    encrypted = encryptor.encrypt(pad_pkcs7).hex()
    ciphertext = rsa.encrypt(guid.encode(), rsa.PublicKey(n,e)).hex()
    return encrypted + ciphertext

def main():
    response = requests.get(
        "https://gcaptcha4.geetest.com/verify",
        params={
            'callback': f"geetest_{round(time.time() * 1000)}",
            'captcha_id': sitekey,
            'client_type': 'web_mobile',
            'lot_number': r_list[1],
            'risk_type': 'word',
            'payload': r_list[2],
            'process_token': r_list[3],
            'payload_protocol': '1',
            'pt': '1',
            'w': encryp(json.dumps(data),guid)
    })
    return json.loads(re.findall(r"\((.*)\)", response.text)[0])
    

if __name__ == "__main__":
    main()
    