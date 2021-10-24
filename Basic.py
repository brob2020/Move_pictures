import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
import shutil

imgDonal = face_recognition.load_image_file('faces/ulrichComp.jpg')
imgDonal = cv2.cvtColor(imgDonal,cv2.COLOR_BGR2RGB)
imgDonalTest = face_recognition.load_image_file('20201219_151029.jpg')
imgDonalTest = cv2.cvtColor(imgDonalTest,cv2.COLOR_BGR2RGB)


# img = cv2.imread(imgDonalTest, 1)
imgDonalTest = cv2.resize(imgDonalTest, (0, 0), fx=0.3, fy=0.3)
imgDonal = cv2.resize(imgDonal, (1, 0), fx=0.3, fy=0.3)

# cv2.imshow('Donald Test ', img)
faceLocTest = face_recognition.face_locations(imgDonalTest)[0]

cv2.waitKey(0)


### find the faces

faceLoc = face_recognition.face_locations(imgDonal)[0]
encodeDonal = face_recognition.face_encodings(imgDonal)[0]

# ## test image
# print (len(face_recognition.face_locations(imgDonalTest)))
# if len(face_recognition.face_locations(imgDonalTest)) > 0:
faceLocTest = face_recognition.face_locations(imgDonalTest)[0]
encodeDonalTest = face_recognition.face_encodings(imgDonalTest)[0]

## draw the rectangle
cv2.rectangle(imgDonal,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
cv2.rectangle(imgDonalTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)

## find if they match

results = face_recognition.compare_faces([encodeDonal],encodeDonalTest)
faceDis = face_recognition.face_distance([encodeDonal],encodeDonalTest)                ## find the best match , the lower it is the better the match
print(faceDis)
cv2.putText(imgDonalTest,f'{results} {round(faceDis[0],2)}',(50,50),cv2.FONT_HERSHEY_SCRIPT_COMPLEX ,1,(0,0,0),2)

cv2.imshow('Donald Trump', imgDonal)
cv2.imshow('Donald Test ', imgDonalTest)
cv2.waitKey(0)
# else :
#     print("out of range ")
#     # os.path.ex
#     if os.path.exists('Nofaces images'):
#         print("directory exist already ......")
#     else:
#         os.makedirs('Nofaces images')
#     shutil.copy("D:/python/faceapp/noFace.jpg", 'Nofaces images/noface.jpg')
#     print("files moved with succes ")
