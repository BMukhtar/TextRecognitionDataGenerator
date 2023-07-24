import sys
sys.path.insert(0, '..')
from trdg.generators import GeneratorFromDict
import random

import os

fonts_folder = "./fonts"
def get_ttf_files(folder):
    ttf_files = []

    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.endswith(".ttf")]:
            ttf_files.append(os.path.join(dirpath, filename))

    return ttf_files

ttf_files = get_ttf_files(fonts_folder)

def generate_margins(n = 100, m = 5):
    res = []
    for i in range(n):
        res.append((random.randint(0, m), random.randint(0, m), random.randint(0, m), random.randint(0, m)))
    return res


from tqdm import tqdm
train_folder = "../../PaddleOCR_Mukhtar/train_data/rec/synthetic/"
relative_train_folder = "./train_data/rec/synthetic/"

# Define train and test split

dict_size = 54064

train_test_split = dict_size

image_count = dict_size * 3
offset = 0



def main():
    generator = GeneratorFromDict(
        blur=1,
        length=1,
        random_blur=True,
        image_dir="./images",
        background_types=[0,1,2,3],
        size=48,
        distorsion_types=[0,1,2,3],
        path="./kk_dict.txt",
        text_colors=["#282828", "#000000", "#333333", "#666666", "#999999", "#1520A6",],
        fonts=ttf_files,
        stroke_widths=[-1, 0, 1],
        character_spacings=[-1, 0, 1, 2, 3],
        stroke_fills=["#282828", "#000000", "#333333", "#666666", "#999999", "#1520A6",],
        margins=generate_margins(),
        random_case=True,
    )

    with open(f"{train_folder}synthetic_test.txt", "a") as test_file, open(f"{train_folder}synthetic_train.txt", "a") as train_file:
        for idx in tqdm(range(offset, image_count)):
            (img, lbl) = generator.next()
            file_name = f"word_{str(idx).zfill(3)}.jpg"
            file_path = f"{train_folder}img/{file_name}"
            img.save(file_path)

            if idx < train_test_split:
                # Write to test file
                test_file.write(f"{file_name}\t{lbl}\n")
            else:
                # Write to train file
                train_file.write(f"{file_name}\t{lbl}\n")


if __name__ == "__main__":
    main()