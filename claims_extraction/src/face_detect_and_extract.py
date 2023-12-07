import cv2
import sys
import os

# imagePath = sys.argv[1]
imagePath = "path/to/input_image"
faceFolderPath = 'path/to/folder'
if not os.path.exists(faceFolderPath):
    os.makedirs(faceFolderPath)

image = cv2.imread(imagePath)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
) 

print("Found {0} Faces!".format(len(faces)))

for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    roi_color = image[y:y + h, x:x + w] 
    print("[INFO] Object found. Saving locally.")
    # cv2.imwrite(str(w) + str(h) + '_faces.jpg', roi_color)
    faces_file_path = os.path.join(faceFolderPath, str(w) + str(h) + '_faces.jpg')
    cv2.imwrite(faces_file_path, roi_color) 

status = cv2.imwrite(rf'{faceFolderPath}/faces_detected.jpg', image)
print ("Image faces_detected.jpg written to filesystem: ",status)