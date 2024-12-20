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
import json
import string
from typing import Dict
import math
import shutil

afterword_symbols = "!?.,:;"
numbers = "0123456789"
other_symbols = string.punctuation + "«»…£€¥¢฿₸₽№°—"
space_symbol = ' '
kazakh_letters = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯЁабвгдежзийклмнопрстуфхцчшщъыьэюяёӘҒҚҢӨҰҮІҺәғқңөұүіһ'
english_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
all_letters = kazakh_letters + english_letters
all_symbols = numbers + other_symbols + space_symbol + all_letters
assert len(all_symbols) == len(set(all_symbols))

all_set = set(all_symbols)

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

from tqdm import tqdm
from queue import Empty

def process_chunk(start_idx, end_idx, generator_params, folder, dict_index, queue):
    generator = GeneratorFromDict(**generator_params)
    local_labels = []
    
    for idx in range(start_idx, end_idx):
        (img, lbl) = generator.next()
        while img is None or set(lbl).issubset(all_set) == False:
            (img, lbl) = generator.next()

        file_name = f"word_{str(dict_index).zfill(1)}_{str(idx).zfill(5)}.jpg"
        file_path = f"{folder}{file_name}"
        img.save(file_path)
        local_labels.append(('./' + file_name, lbl))
        
        if (idx - start_idx + 1) % 100 == 0:
            queue.put(100)
    
    # Report any remaining items
    remaining = (end_idx - start_idx) % 100
    if remaining > 0:
        queue.put(remaining)
    
    return local_labels

def parallelize_generation(dict_size, generator_params, folder, dict_index):
    num_cores = multiprocessing.cpu_count()
    chunk_size = max(1, math.ceil(dict_size / num_cores))
    
    pool = multiprocessing.Pool(processes=num_cores)
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    
    chunks = [(i * chunk_size, min((i + 1) * chunk_size, dict_size)) for i in range(num_cores)]
    
    process_func = partial(process_chunk, 
                           generator_params=generator_params, 
                           folder=folder, 
                           dict_index=dict_index,
                           queue=queue)
    
    results = []
    with tqdm(total=dict_size, desc=f"Dict {dict_index}") as pbar:
        async_results = [pool.apply_async(process_func, chunk) for chunk in chunks]
        
        completed = 0
        epsilon = 0
        empty_wait = 10
        while completed + epsilon < dict_size:
            try:
                progress = queue.get(timeout=5)
                pbar.update(progress)
                completed += progress
                empty_wait = 10
            except Empty:
                if empty_wait < 0:
                    break
                empty_wait = empty_wait - 1
                print("Queue is empty")
                pass
        
        results = [res.get() for res in async_results]
    
    pool.close()
    pool.join()
    
    return [item for sublist in results for item in sublist]  # Flatten the list of results

def dataset(folder: str, dicts):
    # create folder if not exists
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder + "images/", exist_ok=True)

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
        
        dict_labels = parallelize_generation(dict_size, generator_params, folder + "images/", dict_index)
        labels.extend(dict_labels)

    # save to csv file with columns: filename, words with tab separator
    df = pd.DataFrame(labels, columns=["filename", "words"])
    df.to_csv(f"{folder}labels.csv", sep="\t", index=False)
    labels_json = df.set_index('filename')['words'].to_dict()

    with open(f"{folder}labels.json", 'w', encoding='utf-8') as f:
        json.dump(labels_json, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    test_folder = "../../doctr_htr/all_data_combined/test/dtgr_v13_large/"
    train_folder = "../../doctr_htr/all_data_combined/train/dtgr_v13_large/"
    generated_corpus = "../../synthtiger_kz/resources/corpus/kz_corpus_generated.txt"
    real_kz_corpus = "./corpus/corpus_words.txt"
    russian_corpus = "../../synthtiger_kz/resources/corpus/russian.txt"
    test_dicts = [(russian_corpus, 100), (generated_corpus, 100), (real_kz_corpus, 2000)]
    train_dicts = [(russian_corpus, 2000), (generated_corpus, 50000), (real_kz_corpus, 1000000)]
    
    print("Generating test dataset...")
    dataset(test_folder, test_dicts)
    print("Generating train dataset...")
    dataset(train_folder, train_dicts)