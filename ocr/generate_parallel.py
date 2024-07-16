import sys
sys.path.insert(0, '..')
from trdg.generators import GeneratorFromDict
import random
from tqdm import tqdm
import pandas as pd
import logging
import os
import multiprocessing
from functools import partial

logging.basicConfig(level=logging.ERROR)

fonts_folder = "./fonts"

def get_ttf_files(folder):
    ttf_files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.endswith(".ttf")]:
            ttf_files.append(os.path.join(dirpath, filename))
    return ttf_files

ttf_files = get_ttf_files(fonts_folder)

def generate_margins(n=100, m=3):
    return [(random.randint(0, m), random.randint(0, m), random.randint(0, m), random.randint(0, m)) for _ in range(n)]

def process_chunk(start_idx, end_idx, generator_params, folder, dict_index):
    generator = GeneratorFromDict(**generator_params)
    local_labels = []
    
    for idx in range(start_idx, end_idx):
        (img, lbl) = generator.next()
        while img is None:
            (img, lbl) = generator.next()

        file_name = f"word_{str(dict_index).zfill(1)}_{str(idx).zfill(5)}.jpg"
        file_path = f"{folder}{file_name}"
        img.save(file_path)
        local_labels.append(('./' + file_name, lbl))
    
    return local_labels

def parallelize_generation(dict_size, generator_params, folder, dict_index):
    num_cores = multiprocessing.cpu_count() - 1
    chunk_size = max(1, dict_size // num_cores)
    
    pool = multiprocessing.Pool(processes=num_cores)
    
    chunks = [(i * chunk_size, min((i + 1) * chunk_size, dict_size)) for i in range(num_cores)]
    
    process_func = partial(process_chunk, 
                           generator_params=generator_params, 
                           folder=folder, 
                           dict_index=dict_index)
    
    results = []
    with tqdm(total=dict_size, desc=f"Dict {dict_index}") as pbar:
        for result in pool.starmap(process_func, chunks):
            results.extend(result)
            pbar.update(len(result))
    
    pool.close()
    pool.join()
    
    return results

def dataset(folder: str, dicts):
    # clean folder
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))

    labels = []
    for dict_index, (dict_path, dict_size) in enumerate(dicts):
        generator_params = {
            "count": 128,
            "blur": 1,
            "length": 1,
            "allow_variable": False,
            "random_blur": True,
            "random_skew": True,
            "skewing_angle": 10,
            "image_dir": "./backgrounds",
            "background_types": [0,1,2,3],
            "fit": False,
            "alignment": 0,
            "sizes": list(range(20, 49)),
            "distorsion_types": [0,1,2,3],
            "path": dict_path,
            "text_colors": ["#282828", "#000000", "#333333", "#666666", "#999999", "#1520A6"],
            "fonts": ttf_files,
            "stroke_widths": [0, 1],
            "character_spacings": [0, 1, 2, 3],
            "stroke_fills": ["#282828", "#000000", "#333333", "#666666", "#999999", "#1520A6"],
            "margins": generate_margins(),
            "random_case": False,
        }
        
        dict_labels = parallelize_generation(dict_size, generator_params, folder, dict_index)
        labels.extend(dict_labels)

    # save to csv file with columns: filename, words with tab separator
    df = pd.DataFrame(labels, columns=["filename", "words"])
    df.to_csv(f"{folder}labels.csv", sep="\t", index=False)

if __name__ == "__main__":
    test_folder = "../../synthtiger_kz/results/test_v12/dtgr_v3/"
    train_folder = "../../synthtiger_kz/results/train_v12/dtgr_v3/"
    generated_corpus = "../../synthtiger_kz/resources/corpus/kz_corpus_generated.txt"
    russian_corpus = "../../synthtiger_kz/resources/corpus/russian.txt"
    test_dicts = [(generated_corpus, 1000), (russian_corpus, 1000)]
    train_dicts = [(generated_corpus, 500000), (russian_corpus, 50000)]
    
    print("Generating test dataset...")
    dataset(test_folder, test_dicts)
    print("Generating train dataset...")
    dataset(train_folder, train_dicts)