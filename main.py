import time
import FaceRecogniserTest
import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
import newEmailClient
import logging
import base64


UPLOAD_FOLDER = '/tmp'  # for it to work, change it to somewhere in your home directory
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
photoArray=[]
arg1=''
arg2=''
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    photoArray=[]
    if request.method == 'POST' or request.method == 'GET':
        # check if the post request has the file part
        print 'requests.files =', request.files
        for f in 'file1', 'file2':
            if f not in request.files:
                print('No file part')
                return redirect(request.url)
            fobj = request.files[f]
            print 'fobj.filename =', fobj.filename
            # if user does not select file, browser also
            # submit a empty part without filename
            if fobj.filename == '':
                print('No selected file')
                return redirect(request.url)
            if fobj and allowed_file(fobj.filename):
                filename = secure_filename(fobj.filename)
                saveAsFile = f + '_' + filename
                print('received:' + saveAsFile)
                fobj.save(os.path.join(app.config['UPLOAD_FOLDER'], saveAsFile))
                photoFilePath = UPLOAD_FOLDER+'/'+saveAsFile
                photoArray.append(photoFilePath)
        user = request.form.get('username', '')
    print(photoArray)
    try:
        result= FaceRecogniserTest.faceRecogniser(photoArray[0],photoArray[1])
        if (result==[True]):
    	 #success upgrade to premium member
            #print("Sucess, matched!")
            m=newEmailClient.Mailer()
            m.gmail_password = "xxx"
            m.send_from="iAmMeCustomer@gmail.com"
            m.recipients="XXX"
            m.subject="Face Detection Report"
            m.message="Succeed in automated test for "+ user
            m.attachments=photoArray
            m.send_email()
        else:
            #print("Failure, not match")
            m=newEmailClient.Mailer()
            m.gmail_password = "XXX"
            m.send_from="iAmMeCustomer@gmail.com"
            m.recipients="zengersoong@gmail.com"
            m.subject="Face Detection Report"
            m.message="Failed in automated test for " + user
            m.attachments=photoArray
            m.send_email()
            
            #print('username =', request.form.get('username'))  # you can also send other info together
            return 'ok'
    except IndexError as err:
        pass
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file1>
      <p><input type=file name=file2>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/jsonupload', methods=['GET', 'POST'])
def jsonupload_file():
    user = request.form.get('username')
    print(user)
    photoArray=[]
    if request.method == 'POST' or request.method == 'GET':
        # check if the post request has the file part
        for img in 'image1', 'image2':
            if img not in request.json:
                print('No image part', img)
                return redirect(request.url)
            fobjdata = base64.b64decode(request.json[img])
            saveAsFile = img + '_' + str(int(time.time())) + '.jpg'
            print('received:' + saveAsFile)
            photoFilePath = UPLOAD_FOLDER+'/'+saveAsFile
            with open(photoFilePath, 'wb') as fout:
                fout.write(fobjdata)
            photoArray.append(photoFilePath)
        user= request.json.get('user', '')
    print(photoArray)
    try:
        result= FaceRecogniserTest.faceRecogniser(photoArray[0],photoArray[1])
        if (result==[True]):
    	 #success upgrade to premium member
            #print("Sucess, matched!")
            m=newEmailClient.Mailer()
            m.gmail_password = "XXX"
            m.send_from="iAmMeCustomer@gmail.com"
            m.recipients="XXX"
            m.subject="Face Detection Report"
            m.message="Succeed in automated test from user " + user
            m.attachments=photoArray
            m.send_email()
        else:
            #print("Failure, not match")
            m=newEmailClient.Mailer()
            m.gmail_password = "XXX"
            m.send_from="iAmMeCustomer@gmail.com"
            m.recipients="zengersoong@gmail.com"
            m.subject="Face Detection Report"
            m.message="Failed in automated test"+"from user: "+ user
            m.attachments=photoArray
            m.send_email()
            
            #print('username =', request.form.get('username'))  # you can also send other info together
            return 'ok'
        for fn in photoArray:
            os.remove(fn)
    except IndexError as err:
        pass
    except OSError as err:
        print err
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file1>
      <p><input type=file name=file2>
         <input type=submit value=Upload>
    </form>
    '''


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500

if __name__ == '__main__':
       app.run(host='0.0.0.0', debug = True)
