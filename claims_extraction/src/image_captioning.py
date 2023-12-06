import os
from pathlib import Path
import csv
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

data_dir = "../../data/"

count = 0

# iterate through files here
for filename in os.scandir(data_dir):

    pretrained_model_name = "_Salesforce_blip-image-captioning-base"

    out_filename = "image_captioning" + pretrained_model_name + ".csv"
    data_out_name = "data_out"

    out_dir_name = os.path.join("..", "..", data_out_name)
    # create dir if it does not exist
    Path(out_dir_name).mkdir(parents=True, exist_ok=True)

    out_file_path = os.path.join(out_dir_name, out_filename)

    col1_filename = filename.path.split(os.path.sep)[-1]

    processed_files = []
    if os.path.exists(out_file_path):
        with open(out_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                processed_files.append(row[0])

    if filename.is_file() and col1_filename not in processed_files:
        count += 1

        raw_image = Image.open(filename.path).convert('RGB')

        # conditional image captioning
        # text = "a photography of"
        # inputs = processor(raw_image, text, return_tensors="pt")
        # out = model.generate(**inputs, max_new_tokens=20)
        # print(processor.decode(out[0], skip_special_tokens=True))

        # unconditional image captioning
        inputs = processor(raw_image, return_tensors="pt")
        out = model.generate(**inputs, max_new_tokens=20)
        # print(processor.decode(out[0], skip_special_tokens=True))

        data_concat = [col1_filename, processor.decode(out[0], skip_special_tokens=True)]
        # Save output to file
        print("Saving image captioning text:" + str(count))
        with open(out_file_path, 'a', newline='') as csvfile:
            img_cap_writer = csv.writer(csvfile, delimiter=",")
            img_cap_writer.writerow(data_concat)
    else:
        count += 1
        print("Skipping processed file:" + str(count))
