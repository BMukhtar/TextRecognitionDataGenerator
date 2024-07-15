import pandas as pd

test_folder = "../../synthtiger_kz/results/test_v12/dtgr/"
train_folder = "../../synthtiger_kz/results/train_v12/dtgr/"


def shorten_path_of_filename(folder):
    initial = pd.read_csv(f"{folder}labels.csv", sep="\t")
    initial.filename = initial.filename.apply(lambda x: x.split('/')[-1])
    initial.to_csv(f"{folder}labels.csv", sep="\t", index=False)

shorten_path_of_filename(test_folder)
shorten_path_of_filename(train_folder)
