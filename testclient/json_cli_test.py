#!/usr/bin/python

import requests
import json
import base64

#change UPLOAD_URL Accordingly to test

UPLOAD_URL = 'http://localhost:5000/jsonupload'

json_data = { 'user': 'Harry Porter' }

images = [
        ( 'image1', 'testpicts/idpictures/pictureID1.jpeg'), 
        ( 'image2', 'testpicts/facepicture/face1.jpg'), 
        ]
for img, fn in images:
    with open(fn, 'rb') as fin:
        json_data[img] = base64.b64encode(fin.read()).replace('\n', '')
	

#headers = {'Authorization' : , 'Accept' : 'application/json', 'Content-Type' : 'application/json'}
headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}

r = requests.post(UPLOAD_URL, data=json.dumps(json_data), headers=headers)

print r
