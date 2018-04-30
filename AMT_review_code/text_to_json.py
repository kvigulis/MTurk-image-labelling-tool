import os
import json
root = os.getcwd()

text_labels = os.path.join(root,'text_labels')

text_files = os.listdir(text_labels)




for text_file in text_files:
    text_path = os.path.join(text_labels, text_file)
    image_name = text_file.split('_')[0]
    image_name = image_name + '.jpg'
    print('image name:', image_name)
    f = json.load(open(text_path))
    print(f)
    labels = f
    dict = {"image_filename": image_name, "complete": True, "labels": labels}
    print(dict)


    filename_prefix = image_name.split(".")[0]
    full_filename = filename_prefix + "_labels.json"
    file_path = 'text_labels_output/' + full_filename
    print(file_path)
    with open(file_path, 'w') as outfile:
        json.dump(dict, outfile)
    print("=============================================================\n")
