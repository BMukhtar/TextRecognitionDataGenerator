import pandas as pd
from tqdm import tqdm

# Latin to Cyrillic character mapping (substituting similar-looking characters)
latin_to_cyrillic = {
    'a': 'а',  # Latin 'a' -> Cyrillic 'а'
    'A': 'А',  # Latin 'A' -> Cyrillic 'А'
    'e': 'е',  # Latin 'e' -> Cyrillic 'е'
    'E': 'Е',  # Latin 'E' -> Cyrillic 'Е'
    'i': 'і',  # Latin 'i' -> Cyrillic 'і'
    'I': 'І',  # Latin 'I' -> Cyrillic 'І'
    'o': 'о',  # Latin 'o' -> Cyrillic 'о'
    'O': 'О',  # Latin 'O' -> Cyrillic 'О'
    'p': 'р',  # Latin 'p' -> Cyrillic 'р'
    'P': 'Р',  # Latin 'P' -> Cyrillic 'Р'
    'c': 'с',  # Latin 'c' -> Cyrillic 'с'
    'C': 'С',  # Latin 'C' -> Cyrillic 'С'
    'y': 'у',  # Latin 'y' -> Cyrillic 'у'
    'Y': 'У',  # Latin 'Y' -> Cyrillic 'У'
    'x': 'х',   # Latin 'x' -> Cyrillic 'х'
    'X': 'Х',   # Latin 'X' -> Cyrillic 'Х'
    'H': 'Н',  # Latin 'H' -> Cyrillic 'Н'
    'K': 'К',  # Latin 'K' -> Cyrillic 'К'
    'M': 'М',  # Latin 'M' -> Cyrillic 'М'
    'T': 'Т',  # Latin 'T' -> Cyrillic 'Т'
    'B': 'В',  # Latin 'B' -> Cyrillic 'В'
}

# Reverse mapping: Cyrillic to Latin (to handle the inverse direction)
cyrillic_to_latin = {v: k for k, v in latin_to_cyrillic.items()}

trans_table = str.maketrans(latin_to_cyrillic)

# Normalize a word to a standard Latin form by handling both Latin->Cyrillic and Cyrillic->Latin transformations
def normalize_word(word):
    return  word.translate(trans_table)

# Read the CSV data
data = pd.read_csv('./corpus_output/total_words.csv', sep='\t')

# convert word to string
data['word'] = data['word'].astype(str)

# size before
print(data.shape)

# Create a dictionary to store the most frequent word for each normalized form
normalized_dict = {}

# Process each word and count the most frequent occurrence of similar-looking words
for index, row in tqdm(data.iterrows(), total=data.shape[0]):
    word = row['word']
    count = row['count']
    
    # Normalize the word
    normalized_word = normalize_word(word)
    
    # If the normalized word is already in the dictionary, compare counts
    if normalized_word in normalized_dict:
        # Keep the most frequent one
        if normalized_dict[normalized_word][1] < count:
            normalized_dict[normalized_word] = (word, count)
    else:
        normalized_dict[normalized_word] = (word, count)

# Create a final list of words with the highest frequency in each group
final_words = [(word, count) for word, count in normalized_dict.values()]

# Sort by count (highest first)
final_words.sort(key=lambda x: x[1], reverse=True)

# Convert the result to a DataFrame
final_df = pd.DataFrame(final_words, columns=['word', 'count'])

# size after
print(final_df.shape)

# Save or display the final output
final_df.to_csv('./corpus_output/cleaned_words.csv', sep='\t', index=False)




# import modin.pandas as pd

# # Latin to Cyrillic character mapping (substituting similar-looking characters)
# LATIN_TO_CYRILLIC = {
#     'a': 'а',  # Latin 'a' -> Cyrillic 'а'
#     'A': 'А',  # Latin 'A' -> Cyrillic 'А'
#     'e': 'е',  # Latin 'e' -> Cyrillic 'е'
#     'E': 'Е',  # Latin 'E' -> Cyrillic 'Е'
#     'i': 'і',  # Latin 'i' -> Cyrillic 'і'
#     'I': 'І',  # Latin 'I' -> Cyrillic 'І'
#     'o': 'о',  # Latin 'o' -> Cyrillic 'о'
#     'O': 'О',  # Latin 'O' -> Cyrillic 'О'
#     'p': 'р',  # Latin 'p' -> Cyrillic 'р'
#     'P': 'Р',  # Latin 'P' -> Cyrillic 'Р'
#     'c': 'с',  # Latin 'c' -> Cyrillic 'с'
#     'C': 'С',  # Latin 'C' -> Cyrillic 'С'
#     'y': 'у',  # Latin 'y' -> Cyrillic 'у'
#     'Y': 'У',  # Latin 'Y' -> Cyrillic 'У'
#     'x': 'х',   # Latin 'x' -> Cyrillic 'х'
#     'X': 'Х',   # Latin 'X' -> Cyrillic 'Х'
#     'H': 'Н',  # Latin 'H' -> Cyrillic 'Н'
#     'K': 'К',  # Latin 'K' -> Cyrillic 'К'
#     'M': 'М',  # Latin 'M' -> Cyrillic 'М'
#     'T': 'Т',  # Latin 'T' -> Cyrillic 'Т'
#     'B': 'В',  # Latin 'B' -> Cyrillic 'В'
# }


# def create_translation_table():
#     """Create a translation table for Latin to Cyrillic mapping."""
#     return str.maketrans(LATIN_TO_CYRILLIC)

# def normalize_words(words):
#     """
#     Vectorized normalization of words using translation table.
    
#     Args:
#         words (pd.Series): Series of words to normalize
    
#     Returns:
#         pd.Series: Normalized words
#     """
#     # Create translation table
#     trans_table = create_translation_table()
    
#     # Vectorized translation
#     return words.astype(str).apply(lambda x: x.translate(trans_table))

# def normalize_word_frequency(df):
#     """
#     Normalize word frequencies by keeping the most frequent variant.
    
#     Args:
#         df (pd.DataFrame): DataFrame with 'word' and 'count' columns
    
#     Returns:
#         pd.DataFrame: Normalized DataFrame with most frequent words
#     """
#     # Convert to string to ensure consistent processing
#     df = df.copy()
#     df['word'] = df['word'].astype(str)
    
#     # Create normalized word column
#     df['normalized_word'] = normalize_words(df['word'])
    
#     # Group by normalized word and select the most frequent original word
#     normalized_df = (df.sort_values('count', ascending=False)
#                        .groupby('normalized_word')
#                        .first()
#                        .reset_index())
    
#     # Select only word and count columns
#     return normalized_df[['word', 'count']].sort_values('count', ascending=False)

# def main(input_path='./corpus_output/total_words.csv', 
#          output_path='./corpus_output/cleaned_words_fast.csv'):
#     """
#     Main function to process word frequencies.
    
#     Args:
#         input_path (str): Path to input CSV file
#         output_path (str): Path to output CSV file
#     """
#     # Read input file
#     data = pd.read_csv(input_path, sep='\t')
    
#     # Print initial size
#     print(f"Initial DataFrame size: {data.shape}")
    
#     # Normalize word frequencies
#     normalized_data = normalize_word_frequency(data)
    
#     # Print final size
#     print(f"Normalized DataFrame size: {normalized_data.shape}")
    
#     # Save to output file
#     normalized_data.to_csv(output_path, sep='\t', index=False)
    
#     return normalized_data

# if __name__ == '__main__':
#     main()

