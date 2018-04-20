'''
Created on 13 Mar 2018

@author: zenger
'''

from PIL import Image
import face_recognition
import sys
import unittest
import time
import os

#arg1 is directory of photo id , arg2 is directory path of self-portrait, arg3 is type of assertTest 
def main():
    image1 =sys.argv[1]
    image2 =sys.argv[2]
    typeOfTest=sys.argv[3]
    test1 = MyTest()
    test1.test(image1, image2 , typeOfTest)
    
    
class MyTest(unittest.TestCase):
    def test(self,image1,image2,typeOfTest):
        result = faceRecogniser(image1, image2)
        if(typeOfTest=='true'):
            print("Testing... Test is expected to return true")
            self.assertEqual(result, [True])
            print("----------------------The Result is "+ str(result)+"----------------------")
        elif(typeOfTest =='false'):
            print("Testing... Test is expected to return false")
            self.assertEqual(result,[False])
            print("----------------------The Result is "+ str(result)+"----------------------")
        else:
            print("Type of Test not defined")
            
    
    


def faceRecogniser(image1,image2):
    faceFound1=False
    faceFound2=False
    maxRotateLimit1=0
    maxRotateLimit2=0

    while faceFound1==False:
        if(maxRotateLimit1>4):return False
        print("finding face...try#"+str(maxRotateLimit1))
        imageID =face_recognition.load_image_file(image1)
        face_locations = face_recognition.face_locations(imageID)
        if (len(face_locations)<1):
            print("Picture in id require rotating...")
            picture= Image.open(image1)
            picture.rotate(90).save(image1)
            #image1='/home/zenger/uploaded2/image1'
            maxRotateLimit1=+1
        else:
            faceFound1=True
            

    while faceFound2==False:
        if(maxRotateLimit2>4):return False
        print("finding face...try#"+str(maxRotateLimit2))
        imageID2 =face_recognition.load_image_file(image2)
        face_locations2 = face_recognition.face_locations(imageID2)
        if (len(face_locations2)<1):
            print("Portrait picture require rotating...")
            picture= Image.open(image2)
            picture.rotate(90).save(image2)
            #image2='/home/zenger/uploaded2/image2'
            maxRotateLimit2=+1
        else:
            faceFound2=True




    #print("I found {} face(s) in this photograph.".format(len(face_locations)))

    for face_location in face_locations:
        top, right, bottom, left = face_location
    #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
        face_image = imageID[top:bottom , left:right]
        pil_image = Image.fromarray(face_image)
        
        print("Face extracted from ID...")
    #time.sleep(2)
    for face_location2 in face_locations2:
        top2, right2, bottom2, left2 = face_location2
        face_image2 = imageID2[top2:bottom2 , left2:right2]
        pil_image2 = Image.fromarray(face_image2)
        print("Face extracted from photo...")
            
    
        #pil_image.show()
    #save the cropped image into cropped_image
    cropped_image = "/tmp/Trimmed"+time.strftime("%Y%m%d")
    pil_image.save(cropped_image, "png")
    #pil_image.show()
    cropped_image2 = "/tmp/Trimmed2"+time.strftime("%Y%m%d")
    pil_image2.save(cropped_image2, "png")
    #pil_image2.show()
    known_image = face_recognition.load_image_file(cropped_image)
    unknown_image = face_recognition.load_image_file(cropped_image2) # this is from the camera
    known_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    print("Comparing faces...")
    results = face_recognition.compare_faces([known_encoding], unknown_encoding)
    print(results)
    os.remove(cropped_image)
    os.remove(cropped_image2)
    print("Intermediate photos removed.")
    return results
       
        
    # my code here

if __name__ == "__main__":
    main()

