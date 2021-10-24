from deepface import DeepFace
detectors = ['opencv', 'ssd', 'mtcnn', 'dlib']
img = DeepFace.detectFace("20201224_221558.jpg", detector_backend = detectors[0])
print(img)