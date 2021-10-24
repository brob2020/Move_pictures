import face_recognition as fr
import os
import cv2
import face_recognition

## import the image automactly

path = 'faces'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curentImg = cv2.imread(f'{path}/{cl}')
    images.append(curentImg)
    classNames.append(os.path.splitext(cl)[0])
# print(classNames)

## the encoding process

def findEncoding (images):
    encodeList = []
    ii= 0
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if len(face_recognition.face_locations(img)) > 0:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        else:
            print('No face detected in ',myList[ii])
        ii += 1
        print("********************** occulence : ", ii)

    return encodeList

encodeListKnown = findEncoding(images)
print('Encoding complete')
print (encodeListKnown)







# faceLoc = face_recognition.face_locations(imgDonal)[0]
# encodeDonal = face_recognition.face_encodings(imgDonal)[0]
#
# ## test image
# faceLocTest = face_recognition.face_locations(imgDonalTest)[0]
# encodeDonalTest = face_recognition.face_encodings(imgDonalTest)[0]
#
# ## draw the rectangle
# cv2.rectangle(imgDonal,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
# cv2.rectangle(imgDonalTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)

## find if they match

# results = face_recognition.compare_faces([encodeDonal],encodeDonalTest)
# faceDis = face_recognition.face_distance([encodeDonal],encodeDonalTest)



# imgDonal = face_recognition.load_image_file('faces/donald trump.jpg')
# imgDonal = cv2.cvtColor(imgDonal,cv2.COLOR_BGR2RGB)
# imgDonalTest = face_recognition.load_image_file('test.jpg')
# imgDonalTest = cv2.cvtColor(imgDonalTest,cv2.COLOR_BGR2RGB)