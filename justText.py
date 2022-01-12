from PIL.Image import Image
import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
from time import sleep
import codecs
import json
from json import JSONEncoder

from numpy.lib.function_base import append


"""
"""

# ***************************************** TO CONVERT INTO JSON FILE *********************


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


def classify_fae(im, encoded_face):
    """
    will find all of the faces in a given image and label
    them if it knows what they are

    :param im: str of file path
    :return: list of face names
    """
    print("encoding received image .........")
    faces = encoded_face
    
    print(type(encoded_face))
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    print("*********************\nencoding complete thanks :) \n *********** .........")
    print("Drawing rectangles for faces ...........")

    #cv2.namedWindow("output", cv2.WINDOW_NORMAL)
    img = cv2.imread(im, 1)
    
    #img = img[:,:,::-1]

    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(
        img, face_locations)

    face_names = []
    print()

    for face_encoding in unknown_face_encodings:
        print(type(face_encoding))
        print(face_encoding)
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(
            faces_encoded, face_encoding, tolerance=0.5)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(
            faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
        print("these are the detected faces ", face_names)
        print(best_match_index)
        print(face_distances)
        print(matches)
        print(known_face_names)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            cv2.rectangle(img, (left-20, top-20),
                          (right+20, bottom+20), (255, 0, 0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(img, (left-20, bottom - 15),
                          (right+20, bottom+20), (255, 0, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(img, name, (left - 20, bottom + 15),
                        font, 1.0, (255, 255, 255), 2)

    # Display the resulting image
    while True:
        img = cv2.resize(img, (1000, 956))
        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('face_names ', face_names)
            return face_names


def write_json(newData, filename="test.json"):
    if os.path.exists(filename):  # & os.stat(filename).st_size == 0:
        print("****************** we are updating your file............")
        with open(filename, 'r+') as file:
            # First we load existing data into a dict.
            print("loading data........")
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            if type(file_data) == dict:
                file_data.update(newData)
            else:

                if len(newData) > 0:
                    for fs in newData:
                        file_data.append(fs)
                else:
                    print("************ no data to save now ")
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent=4, cls=NumpyArrayEncoder)
    else:
        print("****************** this is your first time **************")
        with open(filename, 'w') as file:
            json.dump(newData, file, indent=4, cls=NumpyArrayEncoder)
            file_data = newData
    return file_data

# fonction to get all files in a folder


def get_images(folder):

    imagees = []
    for dirpath, dirnames, filenames in os.walk(folder):
        print('Current Path:', dirpath)
        print("Directory :", dirnames)
        print('Files: ', filenames)
        print("****** ************** MOVING TO THE NEXT DIRECTORY  *******")
        print("****** ************** ************************** *******/n")
        for f in filenames:

            if f.endswith(".jpg") or f.endswith(".png"):
                imagees.append(f)
            else:
                print(f, "is not an image or is not in the corect format.")
    return imagees

# ******************* FONCTION TO GET FACES IF IT HAVENT BEING DONE ******


def faceMatch(images, data, noFace):  # to find if we already have the encoding
    # Deserialization
   # print((noFace))
    
    print("Started Reading JSON file")
    if len(data) > 0:
        for i in images:
            cl = i.split(".")[0]
            # finding if image have encoding
            try:
                data[cl]
                print(cl, "exist and great job ------------------------")

            except:  # if no match send to new obj
                #print("no macth for ,", cl, ":", cl not in noFace)
                #newfile = noFace[len(noFace)-1]
                if cl not in noFace:
                    print(cl, " est abscent  dans le dossier noface   ")
                    noFace.append(cl)
                else:
                    # print(len(data))
                    print(" ######### we already looked ",
                          cl, " and it has no face")
                    
                    noFace.remove(cl)
                    continue
    else:
        print(" there is no data in the given file, let work it out : ")
        # fi_Encod.append(cl)
        for cl in images:
            cl = cl.split(".")[0]
            noFace.append(cl)

    noFace = list(set(noFace))  # removing duplicates.
    return noFace


# img =face_recognition.load_image_file('20201219_151029.jpg')
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
print("image was resised .......")
# img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)

# FOR LATER USE
u_encoded = {}
u_noface = []
encoded = {}

# vARIABLES UNDEPENDENT : MODIFY THEM TO CHANGE THE CODE

path_Un_Known = "./images"
path_Known = "./faces"
kn_Faces = "encodeKnown.json"
no_Faces_F = "noface.json"
newFaces = "Unknow_faces.json"

# DECLARATION VARIABLES USING OTHER VARIABLES

## getting the needed images 
new_Image    = get_images(path_Un_Known)
known_Images = get_images(path_Known)

##3 reading saved files 
noFaceDetect = write_json(u_noface, filename=no_Faces_F)
know_faces_F = write_json(encoded, filename=kn_Faces)
new_Faces_F  = write_json(u_encoded, filename=newFaces)

### checking if we need to encode  the images or if we have them already.
facesMatches = faceMatch(known_Images,know_faces_F,noFaceDetect)
proc_face    = faceMatch(new_Image, new_Faces_F, noFaceDetect)


""" print("*********----------********* /n", new_Faces_F.keys())
print(know_faces_F.keys()) """


def image_encode(im_Code=u_encoded,image=new_Image ,pathLoc = "./images" , name_Codefile = "Unknow_faces.json",data_file=new_Faces_F,faceMatch= proc_face):

    """ 
    im_Code = coding file for image
    Image = images name 
    path_loc = filees lication 
    name_codefile = name of the file to save 

    """
    for f in image:
        print("************ Processing with ", f, "*******************")
        if f.endswith(".jpg") or f.endswith(".png"):
            files_no_ext = f.split(".")[0]
            if files_no_ext in faceMatch:
                face = fr.load_image_file(pathLoc + '/' + f)
                face = cv2.resize(face, (1000, 956))
                print("removing ext and detecting faces ")
                print('we found :', len(fr.face_encodings(face)), "face(s)")
                if len(fr.face_encodings(face)) > 0:
                    encoding = fr.face_encodings(face)[0]
                    im_Code[files_no_ext] = encoding
                    #saveEncode= encoding
                    # print(im_Code)
                    print("saving data in JSON file   ................")
                    write_json(im_Code, filename=name_Codefile)

                else:
                    print('Warning :  sorry  No face detected in ', f)
                    u_noface.append(files_no_ext)

            else:
                print(" ******** we already have an encoding for :", f)
        else:
            print("**************", f, " is not a valide format*********")
            if f.split(".")[0] in noFaceDetect:
                u_noface.append(f.split(".")[0])

    print("complete getting files ........\n")
    data_file.update(im_Code)

    if len(u_noface) > 0:
        print("SAVING FILE WITH NO FACE \n")
        write_json(u_noface, filename=no_Faces_F)
    else:
        print("there is no new files with no faces ")

    return im_Code


unK_Encoding = new_Faces_F
#unK_Encoding.update(image_encode(image =new_Image))
new_Faces_F.update(image_encode(image =new_Image,))
know_faces_F.update(image_encode(im_Code=encoded,image=known_Images,pathLoc=path_Known,name_Codefile=kn_Faces,data_file=know_faces_F,faceMatch=facesMatches))
#print(unK_Encoding.keys())
# comparing faces


def classify_face(unknown_face_encodings, encoded_face):

    """
    will find all of the faces in a given image and label
    them if it knows what they are

    :param im: str of file path
    :return: list of face names
    """
    print("encoding received image .........")
    faces = encoded_face
    faces_encoded = list(faces.values())
    print("***********************************...........")
    print("***********************************...........")
    print("***********************************...........")
    print("***********************************...........")
    
    known_face_names = list(faces.keys())
    print("********************* \nencoding complete thanks :) \n *********** .........")
    print("working with the unknown faces...........")

    face_names = []
    # print(unknown_face_encodings)
    print(len(unknown_face_encodings))
    for face_encoding in unknown_face_encodings:
        print("************ Processing with ", face_encoding, "*******************")
        #print(unknown_face_encodings[face_encoding])
        u_code =np.array( unknown_face_encodings[face_encoding])
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(
            faces_encoded, u_code, tolerance=0.6)
        name = "Unknown"

         # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(
            faces_encoded, u_code)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
        #print("these are the detected faces ", face_names)
        print(" Best match position " ,best_match_index)
        #print("face distances " , face_distances)
        print("here are the matches " , matches)
        print( "here the faces we know", known_face_names)
        print( "so we think this is the best faces----*******", known_face_names[best_match_index])



    return face_names



print(classify_face(new_Faces_F, know_faces_F))
#print(classify_fae("./images/danger.jpg", new_Faces_F))


# @#### Comparation


""" tetr9 = faceMatch("./images")
print("************",tetr9) """
