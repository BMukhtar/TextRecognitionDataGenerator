import sys
sys.path.insert(0, '..')
from trdg.generators import GeneratorFromDict
import random
from tqdm import tqdm
import pandas as pd
import logging
logging.basicConfig(level=logging.ERROR)

import os

fonts_folder = "./fonts"
def get_ttf_files(folder):
    ttf_files = []

    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.endswith(".ttf")]:
            ttf_files.append(os.path.join(dirpath, filename))

    return ttf_files

ttf_files = get_ttf_files(fonts_folder)

def generate_margins(n = 100, m = 3):
    res = []
    for i in range(n):
        res.append((random.randint(0, m), random.randint(0, m), random.randint(0, m), random.randint(0, m)))
    return res

def dataset(folder: str, dicts):
    # clean folder
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))

    labels = []
    for dict_index, (dict_path, dict_size) in enumerate(dicts):
        generator = GeneratorFromDict(
            blur=1,
            length=1,
            allow_variable=False,
            random_blur=True,
            random_skew=True,
            skewing_angle=10,
            image_dir="./backgrounds",
            background_types=[0,1,2,3],
            # all sizes from 12 to 48
            sizes= list(range(20, 49)),
            distorsion_types=[0,1,2,3],
            path=dict_path,
            text_colors=["#282828", "#000000", "#333333", "#666666", "#999999", "#1520A6",],
            fonts=ttf_files,
            stroke_widths=[0, 1, 2],
            character_spacings=[0, 1, 2, 3],
            stroke_fills=["#282828", "#000000", "#333333", "#666666", "#999999", "#1520A6",],
            margins=generate_margins(),
            random_case=False,
        )
        for idx in tqdm(range(dict_size)):
            (img, lbl) = generator.next()
            while img is None:
                (img, lbl) = generator.next()

            file_name = f"word_{str(dict_index).zfill(1)}_{str(idx).zfill(5)}.jpg"
            file_path = f"{folder}{file_name}"
            img.save(file_path)
            labels.append(('./' + file_name, lbl))
    # save to csv file with columns: filename, words with tab separator
    df = pd.DataFrame(labels, columns=["filename", "words"])
    df.to_csv(f"{folder}labels.csv", sep="\t", index=False)


test_folder = "../../synthtiger_kz/results/test_v12/dtgr/"
train_folder = "../../synthtiger_kz/results/train_v12/dtgr/"
generated_corpus = "../../synthtiger_kz/resources/corpus/kz_corpus_generated.txt"
russian_corpus = "../../synthtiger_kz/resources/corpus/russian.txt"
test_dicts = [(generated_corpus, 1000), (russian_corpus, 1000)]
train_dicts = [(generated_corpus, 50000), (russian_corpus, 50000)]
dataset(test_folder, test_dicts)
dataset(train_folder, train_dicts)