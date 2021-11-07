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


def get_encoded_faces():
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}
    print(" calling get_encoded_faces ............ ")

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            print(" Processing  with ", f)
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                print("removing ext and detecting faces ")
                print('we founded :', len(fr.face_encodings(face)))
                if len(fr.face_encodings(face)) > 0:
                    encoding = fr.face_encodings(face)[0]
                    encoded[f.split(".")[0]] = encoding
                    print("Nice ................")
                else:
                    print('#########No face detected in ', f)
        print("complete getting files ........")

    return encoded


def unknown_image_encoded(img):
    """
    encode a face given the file name
    """
    print("*****encoding new files ")
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(im, encoded_face):
    """
    will find all of the faces in a given image and label
    them if it knows what they are

    :param im: str of file path
    :return: list of face names
    """
    print("encoding received image .........")
    faces = encoded_face
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())
    print("*********************\nencoding complete thanks :) \n *********** .........")
    print("working with the unknown faces...........")

    img = cv2.imread(im, 1)
    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    #img = img[:,:,::-1]

    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(
        img, face_locations)

    face_names = []

    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(
            faces_encoded, face_encoding, tolerance=0.6)
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

##### fonction to get all files in a folder 
def get_images(folder):
     
    imagees = []
    for dirpath,dirnames,filenames in  os.walk(folder):
        print('Current Path:',dirpath)
        print("Directory :" ,dirnames)
        print('Files: ',filenames)
        print("****** ************** MOVING TO THE NEXT DIRECTORY  *******")
        print("****** ************** ************************** *******/n")
        for f in filenames:
            
            if f.endswith(".jpg") or f.endswith(".png"):
                imagees.append(f)
            else:
                print(f, "is not an image or is not in the corect format.")
    return imagees

#### ******************* FONCTION TO GET FACES IF IT HAVENT BEING DONE ******

def faceMatch(images, data, noFace):  # to find if we already have the encoding
    # Deserialization
    print(type(noFace))
    print(noFace)
    print("Started Reading JSON file")
    if len(data) > 0:
        for i in images:
            cl = i.split(".")[0]
            # finding if image have encoding
            try:
                data[cl]

            except:  # if no match send to new obj
                #print("no macth for ,", cl, ":", cl not in noFace)
                #newfile = noFace[len(noFace)-1]
                if cl not in noFace:
                    print(cl, " est abscent  dans le dossier noface   ")
                    noFace.append(cl)
                else:
                    #print(len(data))
                    print(" ######### we already looked ",
                          cl, " and it has no face")
                    print(noFace)
                    noFace.remove(cl)
                    continue
    else:
        print(" there is no data in the given file, let work it out : ")
        # fi_Encod.append(cl)
        for cl in images:
            cl = cl.split(".")[0]
            noFace.append(cl)

    noFace = list(set(noFace))  ## removing duplicates.
    return noFace


# img =face_recognition.load_image_file('20201219_151029.jpg')
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
print("image was resised .......")
# img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)


u_encoded = {}
u_noface = []
encoded = []


pathKnown = "./images"
kn_Faces = "encodeKnown.json"
no_Faces_F = "noface.json"
newFaces = "Unknow_faces.json"
image = get_images(pathKnown)
noFaceDetect = write_json(u_noface, filename=no_Faces_F)
know_faces_F = write_json(encoded, filename=kn_Faces)
new_Faces_F = write_json(u_encoded, filename=newFaces)
proc_face = faceMatch(image, new_Faces_F, noFaceDetect)

print(new_Faces_F.keys())


#for dirpath, dnames, fnames in os.walk(pathKnown):
for f in image:
    print("************ Processing with ", f, "*******************")
    if f.endswith(".jpg") or f.endswith(".png"):
        files_no_ext = f.split(".")[0]
        if files_no_ext in proc_face:
            face = fr.load_image_file(pathKnown + '/' + f)
            print("removing ext and detecting faces ")
            print('we found :', len(fr.face_encodings(face)), "face(s)")
            if len(fr.face_encodings(face)) > 0:
                encoding = fr.face_encodings(face)[0]
                u_encoded[files_no_ext] = encoding
                #saveEncode= encoding
                # print(u_encoded)
                print("saving data in JSON file   ................")
                write_json(u_encoded, filename=newFaces)

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

if len(u_noface) > 0:
    print("SAVING FILE WITH NO FACE \n")
    write_json(u_noface, filename=no_Faces_F)
else:
    print("there is no new files with no faces ")


#print(classify_face('./images/noFace.jpg', loadFile))



# @#### Comparation


""" tetr9 = faceMatch("./images")
print("************",tetr9) """
