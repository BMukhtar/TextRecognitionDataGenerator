import pandas as pd
import re
import json

# Create a mapping of similar-looking characters between Cyrillic and Latin
latin_to_cyrillic = {
    'a': 'а',  # Latin 'a' -> Cyrillic 'а'
    'e': 'е',  # Latin 'e' -> Cyrillic 'е'
    'i': 'і',  # Latin 'i' -> Cyrillic 'і'
    'o': 'о',  # Latin 'o' -> Cyrillic 'о'
    'p': 'р',  # Latin 'p' -> Cyrillic 'р'
    'c': 'с',  # Latin 'c' -> Cyrillic 'с'
    'y': 'у',  # Latin 'y' -> Cyrillic 'у'
    'x': 'х'   # Latin 'x' -> Cyrillic 'х'
}

cyrillic_to_latin = {v: k for k, v in latin_to_cyrillic.items()}  # Reverse the mapping

# Function to determine if a word is predominantly Cyrillic
def is_cyrillic_word(word):
    # Count the number of Cyrillic and Latin characters in the word
    cyrillic_count = sum(1 for char in word if re.match(r'[а-яА-ЯёЁ]', char))
    latin_count = sum(1 for char in word if re.match(r'[a-zA-Z]', char))
    
    return cyrillic_count > latin_count

# Function to update characters in a word based on the context
def update_label(word):
    word = str(word)
    if is_cyrillic_word(word):
        # Replace Latin characters with Cyrillic equivalents
        return ''.join(latin_to_cyrillic.get(char, char) for char in word)
    else:
        # Replace Cyrillic characters with Latin equivalents
        return ''.join(cyrillic_to_latin.get(char, char) for char in word)

# # Load the CSV file
# csv_file = 'your_file.csv'  # Replace with your CSV file path
# df = pd.read_csv(csv_file)

# # Process each row in the 'label' column
# df['label'] = df['label'].apply(update_label)

# # Save the updated DataFrame to a new CSV file
# output_file = 'updated_labels.csv'  # Define the output file path
# df.to_csv(output_file, index=False)

# print(f"Labels updated successfully and saved to {output_file}.")

test_folder = "../../doctr_htr/all_data_combined/test/dtgr_v13_large/"
train_folder = "../../doctr_htr/all_data_combined/train/dtgr_v13_large/"
folders = [test_folder, train_folder]
for folder in folders:
    # Load the CSV file
    csv_file = f"{folder}labels.csv"
    df = pd.read_csv(csv_file, sep="\t")

    # Process each row in the 'words' column
    df['words'] = df['words'].apply(update_label)

    # Save the updated DataFrame to a new CSV file
    output_file = f"{folder}labels.csv"
    df.to_csv(output_file, sep="\t", index=False)

    print(f"Labels in {csv_file} updated successfully and saved to {output_file}.")

    labels_json = df.set_index('filename')['words'].to_dict()

    with open(f"{folder}labels.json", 'w', encoding='utf-8') as f:
        json.dump(labels_json, f, ensure_ascii=False, indent=4)
    
    print(f"Labels JSON file saved to {folder}labels.json.")
