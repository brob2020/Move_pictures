import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np

def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        ii =0
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = face_recognition.load_image_file("faces/" + f)
                img = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                if len(face_recognition.face_encodings(img)) > 0:
                    encoding = fr.face_encodings(img)[0]
                    encoded[f.split(".")[0]] = encoding
                    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

                    # cv2.imshow('Donald Test ', img)
                    faceLocTest = face_recognition.face_locations(img)[0]
                    encodeDonalTest = face_recognition.face_encodings(img)[0]
                    cv2.rectangle(img, (faceLocTest[3], faceLocTest[0]), (faceLocTest[1], faceLocTest[2]),(255, 0, 255), 2)
                    cv2.imshow(f, img)
                    cv2.waitKey(10)
                else:
                    print('No face detected in ',f )
                ii += 1
                print("********************** completed for  : ",f)


    return encoded
print(get_encoded_faces())
# mylist = os.listdir("D:\python\Photo_Face\photos")
# withName = os.walk("D:/python/Photo_Face/photos")
# newFace = { }
#
# for dirpath,dirnames,filenames in  withName:
#     print('Current Path:',dirpath)
#     print("Directory :" ,dirnames)
#     print('Files: ',filenames)
#     print()
#     for f in filenames:
#         if f.endswith(".jpg") or f.endswith(".png"):        # VERIFIER L'EXTENSION
#             face = fr.load_image_file(dirpath+'/'+f)
#             print(len(fr.face_encodings(face)))
#             if len(fr.face_encodings(face)) > 0:            ## VERIFIER S'IL YA UNE FACE
#                 encoding = fr.face_encodings(face)[0]
#                 newFace[f.split(".")[0]] = encoding
#                 print("######################### WE DETECTED A FACE ON ", f)
#             else:
#                 print('No face detected in ',f )
#
#             print("********************** completed for  : ",f)
#         print("files name is :",f)
#     print("PROCESS COMPLETED ")

def unknown_image_encoded(img):
    """
    encode a face given the file name
    """

    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding