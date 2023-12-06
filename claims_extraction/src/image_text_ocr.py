import os
import cv2
import pytesseract
from pathlib import Path
import csv

data_dir = "../../data/"

count = 0

# iterate through files here
for filename in os.scandir(data_dir):

    config_psm = 6
    config_oem = 1

    out_filename = "ocr" + "_psm" + str(config_psm) + "_oem" + str(config_oem) + ".csv"
    data_out_name = "data_out"

    out_dir_name = os.path.join("..", "..", data_out_name)
    # create dir if it does not exist
    Path(out_dir_name).mkdir(parents=True, exist_ok=True)

    out_file_path = os.path.join(out_dir_name, out_filename)

    col1_filename = filename.path.split(os.path.sep)[-1]

    processed_files = []
    with open(out_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            processed_files.append(row[0])

    if filename.is_file() and col1_filename not in processed_files:
        count += 1
        image = cv2.imread(filename.path)

        '''
        ## Preprocessing
        # This is making text quality worse
        # Grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Gaussian blur
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        # Otsu's threshold
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        # Morphological ops - remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening
        '''

        # OCR
        # --psm: 6    Assume a single uniform block of text
        # --oem: 1    Neural nets LSTM engine only.
        data = pytesseract.image_to_string(image, lang='eng+hin', config='--psm 6 --oem 1')

        '''
        cv2.imshow('thresh', thresh)
        cv2.imshow('opening', opening)
        cv2.imshow('invert', invert)
        cv2.waitKey()
        '''

        data_concat = [col1_filename, data]
        # Save output to file
        print("Saving OCR text:" + str(count))
        with open(out_file_path, 'a', newline='') as csvfile:
            ocr_writer = csv.writer(csvfile, delimiter=",")
            ocr_writer.writerow(data_concat)
    else:
        count += 1
        print("Skipping processed file:" + str(count))
