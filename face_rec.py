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


def classify_face(im):
    """
    will find all of the faces in a given image and label
    them if it knows what they are

    :param im: str of file path
    :return: list of face names
    """
    print("encoding received image .........")
    faces = get_encoded_faces()
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
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(
            faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        print('matches', matches[best_match_index])
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
        print("these are the detected faces ", face_names)

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


def faceMatch(path, data, noFace):  # to find if we already have the encoding
    # Deserialization
    print(type(noFace))
    print(noFace)
    print("Started Reading JSON file")
    myList = os.listdir(path)
    fi_Encod = []
    if len(data) > 0:
        for i in myList:
            cl = i.split(".")[0]
            # finding if image have encoding
            try:
                data[cl]

            except:  # if no match send to new obj
                print("no macth for ,", cl, ":", cl not in noFace)
                #newfile = noFace[len(noFace)-1]
                if cl not in noFace:
                    print(cl, " est abscent  dans le dossier noface   ")
                    noFace.append(cl)
                else:
                    print(len(data))
                    print(" ######### we already looked ",
                          cl, " and it has no face")
                    print(noFace)
                    noFace.remove(cl)
                    continue
    else:
        print(" there is no data in the given file, let work it out : ")
        # fi_Encod.append(cl)
        for cl in myList:
            cl = cl.split(".")[0]
            noFace.append(cl)

    noFace = list(set(noFace))
    return noFace


# img =face_recognition.load_image_file('20201219_151029.jpg')
# img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
print("image was resised .......")
# img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)


u_encoded = {}
u_noface = []


pathKnown = "./images"
fileName = "encodeKnown.json"
fileNameN = "noface.json"
noFaceDetect = write_json(u_noface, filename=fileNameN)
loadFile = write_json(u_encoded, filename=fileName)
proc_face = faceMatch(pathKnown, loadFile, noFaceDetect)
print(loadFile.keys())


for dirpath, dnames, fnames in os.walk(pathKnown):
    for f in fnames:
        print("************ Processing with ", f, "*******************")
        if f.endswith(".jpg") or f.endswith(".png"):
            fileslip = f.split(".")[0]
            if fileslip in proc_face:
                face = fr.load_image_file(pathKnown + '/' + f)
                print("removing ext and detecting faces ")
                print('we found :', len(fr.face_encodings(face)), "face(s)")
                if len(fr.face_encodings(face)) > 0:
                    encoding = fr.face_encodings(face)[0]
                    u_encoded[fileslip] = encoding
                    #saveEncode= encoding
                    # print(u_encoded)
                    print("saving data in JSON file   ................")
                    write_json(u_encoded, filename=fileName)
                    """  with open('encodeKnown.json', 'w') as write_file:
                        json.dump(u_encoded,write_file ,cls=NumpyArrayEncoder) """

                else:
                    print('Warning :  sorry  No face detected in ', f)
                    u_noface.append(fileslip)

            else:
                print(" ******** we already have an encoding for :", f)
        else:
            print("**************", f, " is not a valide format*********")
            if f.split(".")[0] in  noFaceDetect :
                u_noface.append(f.split(".")[0])


    print("complete getting files ........\n")
print("SAVING FILE WITH NO FACE \n")
if len(u_noface) > 0:
    write_json(u_noface, filename=fileNameN)
else:
    print("there is no new files with no faces ")


""" u_cooode = {'2test74': ([-2.1312435,  0.04238239,  0.09264351, -0.00060404, -0.0332113,
                         -0.09859727,  0.07820927, -0.07746867,  0.10005408, -0.09410999,
                         0.27047098, -0.06461874, -0.17198321, -0.15847702,  0.14748688,
                         0.16749436, -0.12602326, -0.14185981, -0.11033729, -0.12198558,
                         -0.05012843,  0.02010918, -0.06594256,  0.10428463, -0.08432277,
                         -0.31178731, -0.08503884, -0.11321349,  0.07470773, -0.07346639,
                         0.02238713,  0.09271666, -0.1925531, -0.04001348, -0.02827353,
                         0.02777403, -0.00911854, -0.01243259,  0.20587951,  0.05742529,
                         -0.17188711, -0.01984953, -0.05645976,  0.31036186,  0.15637027,
                         -0.05658457,  0.00706496,  0.05435834,  0.04624629, -0.19890812,
                         0.01815106,  0.10775388,  0.13556615,  0.03282607, -0.04539447,
                         -0.09087323, -0.05875951,  0.03323557, -0.24461775,  0.03785361,
                         0.06998263, -0.18959822, -0.13240096, -0.07109768,  0.27155951,
                         0.09406982, -0.1007029, -0.15719123,  0.22491074, -0.15232499,
                         -0.02076321,  0.09252237, -0.13339864, -0.09672306, -0.28084165,
                         0.15382926,  0.33761668,  0.06768966, -0.20568748,  0.00533057,
                         -0.16136867,  0.01243965,  0.00853193,  0.0592257, -0.01133567,
                         0.02356816, -0.05522916,  0.03702855,  0.13861924, -0.00864843,
                         -0.03006561,  0.23610552,  0.01029547, -0.0113841,  0.03967608,
                         -0.08384658,  0.04687623, -0.09172656, -0.07582787, -0.01717666,
                         0.03255101, -0.09929667,  0.03193368,  0.09368521, -0.17329919,
                         0.21345963,  0.03672818,  0.01236537,  0.02483196,  0.09251186,
                         -0.11380426, -0.11736722,  0.15980151, -0.22893035,  0.1585985,
                         0.15846471,  0.06064278,  0.08803577, -0.0134102,  0.1062394,
                         -0.09327123, -0.03116863, -0.14954323, -0.00960312,  0.11461105,
                         -0.0267543,  0.03543857,  0.05331506]), '20201224_221558 kjy': ([-9.17172506e-02,  1.06096439e-01,  1.08179845e-01, -6.81564733e-02,
                                                                                          -7.35871047e-02, -9.28284377e-02,  8.01842660e-04, -1.15273945e-01,
                                                                                          1.82538450e-01, -1.50463030e-01,  2.85217255e-01, -4.08754274e-02,
                                                                                          -1.61894873e-01, -1.25618339e-01,  5.44990450e-02,  2.01620206e-01,
                                                                                          -2.12131351e-01, -1.80235848e-01,  2.43732799e-03, -6.04828112e-02,
                                                                                          -6.35604933e-03,  3.94282863e-03,  3.76237705e-02,  1.38172209e-01,
                                                                                          -1.33037135e-01, -4.21956748e-01, -1.07983708e-01, -1.71163797e-01,
                                                                                          6.45352602e-02, -1.64660588e-02, -3.09246071e-02,  1.47782579e-01,
                                                                                          -2.38988012e-01, -4.20601405e-02, -2.89941914e-02,  2.85927504e-02,
                                                                                          1.85203506e-03, -3.44384462e-02,  1.51457012e-01,  6.29015863e-02,
                                                                                          -2.10579008e-01, -4.10828069e-02,  9.81800258e-06,  2.69155920e-01,
                                                                                          1.16919920e-01, -4.15770486e-02,  6.78926557e-02, -1.78097691e-02,
                                                                                          4.28137928e-03, -1.81681976e-01,  6.28533587e-03,  1.04937129e-01,
                                                                                          1.28109321e-01,  1.89412385e-03,  5.26785478e-03, -1.41355932e-01,
                                                                                          -5.20779528e-02,  4.09260169e-02, -1.79639384e-01,  5.38401417e-02,
                                                                                          1.56421941e-02, -8.22059959e-02, -8.08597207e-02, -9.58169699e-02,
                                                                                          3.40421230e-01,  1.44064903e-01, -1.49272874e-01, -5.63826561e-02,
                                                                                          1.87732309e-01, -1.23205595e-01, -4.07305993e-02,  2.20120400e-02,
                                                                                          -1.52893960e-01, -1.16732486e-01, -2.84108818e-01,  3.26966085e-02,
                                                                                          3.72391105e-01,  6.17529079e-02, -2.18655959e-01,  2.88002864e-02,
                                                                                          -1.41229615e-01, -5.60509879e-03,  1.78077165e-03,  1.94918379e-01,
                                                                                          -5.60379997e-02,  6.45162091e-02, -2.86831725e-02,  3.21935005e-02,
                                                                                          1.34798750e-01, -3.31000425e-02,  7.75100570e-03,  2.53049850e-01,
                                                                                          -5.25362864e-02,  9.48503986e-02,  2.66516302e-03, -6.96607679e-02,
                                                                                          -5.33764586e-02, -6.64937720e-02, -1.16804458e-01, -7.15005770e-03,
                                                                                          -8.48953798e-02, -4.00608778e-02, -8.08303580e-02,  1.13762066e-01,
                                                                                          -1.75676778e-01,  7.18923062e-02,  6.37011155e-02, -4.63599339e-02,
                                                                                          3.08369994e-02,  1.39245644e-01, -7.97864273e-02, -2.09519550e-01,
                                                                                          9.05375108e-02, -2.03409940e-01,  1.52369156e-01,  2.04125986e-01,
                                                                                          1.92548856e-02,  1.52802944e-01,  4.93610092e-02,  8.19663033e-02,
                                                                                          -4.33377624e-02, -5.66117465e-02, -1.49118081e-01,  2.03022584e-02,
                                                                                          1.54526338e-01, -1.13617837e-01, -1.52980573e-02, -2.41881218e-02]), '20201225_114337': ([-1.32869884e-01,  1.10753886e-01,  9.89482552e-02, -1.91224683e-02,
                                                                                                                                                                                    -4.55825925e-02, -1.64241180e-01,  1.28783789e-02, -1.37373403e-01,
                                                                                                                                                                                    1.12589620e-01, -1.18201301e-01,  2.66714483e-01, -1.97003521e-02,
                                                                                                                                                                                    -1.27995208e-01, -1.05450854e-01,  7.28406459e-02,  2.11353809e-01,
                                                                                                                                                                                    -1.84850276e-01, -1.46468773e-01, -7.61504769e-02, -8.21531117e-02,
                                                                                                                                                                                    2.96264067e-02,  3.08805294e-02, -1.62919108e-02,  1.56838194e-01,
                                                                                                                                                                                    -1.10193394e-01, -3.09700608e-01, -1.14227459e-01, -1.74476817e-01,
                                                                                                                                                                                    2.56586634e-02, -6.30763397e-02,  5.40830288e-03,  1.05498396e-01,
                                                                                                                                                                                    -1.81532905e-01,  1.12316040e-02, -2.99857557e-02,  7.18117133e-03,
                                                                                                                                                                                    5.08538410e-02, -2.14293189e-02,  1.65018931e-01,  6.02960363e-02,
                                                                                                                                                                                    -2.13777974e-01,  2.62439847e-02, -4.01098281e-04,  2.89764822e-01,
                                                                                                                                                                                    1.29870772e-01, -7.28785619e-02,  5.63003123e-02, -3.37161906e-02,
                                                                                                                                                                                    1.67365130e-02, -1.45636052e-01,  1.94807835e-02,  6.77011833e-02,
                                                                                                                                                                                    1.59393147e-01, -5.98593149e-03,  1.05760563e-02, -1.49520695e-01,
                                                                                                                                                                                    -5.00579476e-02,  2.22896039e-02, -2.23241657e-01,  6.35745078e-02,
                                                                                                                                                                                    5.84712774e-02, -1.21035568e-01, -1.37678832e-01, -8.15665647e-02,
                                                                                                                                                                                    2.96134919e-01,  1.64870471e-01, -1.50011778e-01, -8.29464048e-02,
                                                                                                                                                                                    1.89887047e-01, -1.09710597e-01, -4.25370745e-02,  8.44698623e-02,
                                                                                                                                                                                    -1.58577874e-01, -1.05924234e-01, -2.71377355e-01,  4.36528735e-02,
                                                                                                                                                                                    3.86466146e-01,  3.77427265e-02, -2.53055304e-01, -8.43686424e-03,
                                                                                                                                                                                    -1.83739111e-01,  1.10266153e-02, -9.14096367e-04,  1.01496778e-01,
                                                                                                                                                                                    -6.38151467e-02,  2.14961246e-02, -6.62126988e-02,  9.45262387e-02,
                                                                                                                                                                                    1.41982064e-01, -1.23101538e-02,  2.10312894e-03,  2.41703644e-01,
                                                                                                                                                                                    -1.78237036e-02,  1.88514590e-04, -3.94466184e-02, -5.10187633e-02,
                                                                                                                                                                                    -2.35294923e-02, -9.00491774e-02, -6.72192723e-02, -5.44824600e-02,
                                                                                                                                                                                    -4.84429020e-03, -6.23785853e-02, -5.53036556e-02,  1.07831925e-01,
                                                                                                                                                                                    -2.10137725e-01,  1.00457981e-01,  7.36704618e-02, -3.22349966e-02,
                                                                                                                                                                                    1.28853256e-02,  1.40767917e-01, -1.15893796e-01, -1.13032743e-01,
                                                                                                                                                                                    1.24249175e-01, -1.86421216e-01,  1.81357220e-01,  1.64626852e-01,
                                                                                                                                                                                    1.63558181e-02,  7.74323419e-02, -1.30269062e-02,  8.56378898e-02,
                                                                                                                                                                                    -1.07731797e-01, -9.85690057e-02, -1.66814312e-01,  2.96311751e-02,
                                                                                                                                                                                    1.71179175e-01, -6.94213733e-02,  4.40061353e-02,  3.59068718e-03]), 'ulrich': ([-0.09719775,  0.10163064,  0.13659304,  0.00556855,  0.00499198,
                                                                                                                                                                                                                                                                     -0.11064501,  0.07038958, -0.06563545,  0.13894604, -0.10144398,
                                                                                                                                                                                                                                                                     0.24667509, -0.03753544, -0.18597519, -0.15524307,  0.07459434,
                                                                                                                                                                                                                                                                     0.16663246, -0.11977261, -0.15885071, -0.11444968, -0.13296144,
                                                                                                                                                                                                                                                                     -0.01845806,  0.03354292, -0.00485847,  0.0726596, -0.06308639,
                                                                                                                                                                                                                                                                     -0.22537889, -0.1261602, -0.15804851,  0.06824638, -0.11040423,
                                                                                                                                                                                                                                                                     0.03222602,  0.06152359, -0.1729961, -0.07144864, -0.03522655,
                                                                                                                                                                                                                                                                     0.00645467,  0.05593374, -0.00801155,  0.17780966,  0.01185397,
                                                                                                                                                                                                                                                                     -0.11809092, -0.02955527,  0.00110796,  0.27149177,  0.18435939,
                                                                                                                                                                                                                                                                     -0.0359551,  0.01339394,  0.01125271,  0.09378875, -0.18331873,
                                                                                                                                                                                                                                                                     0.01265622,  0.05524626,  0.1941583,  0.10908663, -0.0380411,
                                                                                                                                                                                                                                                                     -0.12178588,  0.00314494,  0.04256719, -0.23555943,  0.09333136,
                                                                                                                                                                                                                                                                     0.05682012, -0.18805014, -0.11086406,  0.05016618,  0.27257854,
                                                                                                                                                                                                                                                                     0.09228205, -0.12074023, -0.18091592,  0.18164635, -0.19550769,
                                                                                                                                                                                                                                                                     -0.01385006,  0.15711859, -0.13171786, -0.01561328, -0.299339,
                                                                                                                                                                                                                                                                     0.09414606,  0.38152999,  0.03081921, -0.19640908, -0.02501697,
                                                                                                                                                                                                                                                                     -0.18210593,  0.04374073, -0.05380809,  0.08163497, -0.10309867,
                                                                                                                                                                                                                                                                     0.02877268, -0.12465424,  0.01330984,  0.13920429, -0.01524066,
                                                                                                                                                                                                                                                                     -0.07584088,  0.21230347,  0.01231213,  0.04911534,  0.03729201,
                                                                                                                                                                                                                                                                     -0.00635761,  0.00730604, -0.13262497, -0.04911977, -0.03745692,
                                                                                                                                                                                                                                                                     -0.00308053, -0.09007727, -0.034791,  0.07483035, -0.1119486,
                                                                                                                                                                                                                                                                     0.16456583, -0.01995307,  0.02528764, -0.0559591,  0.09084293,
                                                                                                                                                                                                                                                                     -0.06870716, -0.08706555,  0.15165669, -0.19294617,  0.12820314,
                                                                                                                                                                                                                                                                     0.14349632, -0.01106741,  0.07473274, -0.01423119,  0.15991867,
                                                                                                                                                                                                                                                                     -0.11425548, -0.04044149, -0.05986154, -0.03213088,  0.08312793,
                                                                                                                                                                                                                                                                     -0.01533562,  0.08468633,  0.025687])}

test = {}
y = {'4test': ([-2.1312435,  0.04238239,  0.09264351, ])}
data= write_json(test,filename="danger.json")
print(data) """
# write_json(u_cooode,filename="danger.json")


# print(classify_face('./images/20201225_114337.jpg'))


# @#### Comparation


""" tetr9 = faceMatch("./images")
print("************",tetr9) """
