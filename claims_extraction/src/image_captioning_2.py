from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image
import os
import csv
from pathlib import Path

model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}


def predict_step(image_path):
    i_image = Image.open(image_path)
    if i_image.mode != "RGB":
        i_image = i_image.convert(mode="RGB")

    pixel_values = feature_extractor(images=[i_image], return_tensors="pt").pixel_values
    pixel_values = pixel_values.to(device)

    output_ids = model.generate(pixel_values, **gen_kwargs)

    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]
    return preds


data_dir = "../../data/"

count = 0

# iterate through files here
for filename in os.scandir(data_dir):

    pretrained_model_name = "_nlpconnect_vit-gpt2-image-captioning"

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

        prediction = predict_step(filename.path)
        data_concat = [col1_filename, prediction[0]]
        # Save output to file
        print("Saving image captioning text:" + str(count))
        with open(out_file_path, 'a', newline='') as csvfile:
            img_cap_writer = csv.writer(csvfile, delimiter=",")
            img_cap_writer.writerow(data_concat)
    else:
        count += 1
        print("Skipping processed file:" + str(count))
