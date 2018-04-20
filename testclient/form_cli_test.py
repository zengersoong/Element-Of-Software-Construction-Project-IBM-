#!/usr/bin/python

import requests

url = 'http://localhost:5000/upload'

multiple_files = [
        ('file1', ('image1.jpg', open('testpicts/idpictures/pictureID1.jpeg', 'rb').read(), 'image/jpg')),
        ('file2', ('image2.jpg', open('testpicts/facepicture/face1.jpg', 'rb').read(), 'image/jpg'))]

formdata = { 'username': 'Harry Porter' }
r = requests.post(url, data=formdata, files=multiple_files)
