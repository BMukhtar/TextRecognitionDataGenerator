import os
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

def check_font_support(font_path, characters):
    """Checks if a TTF font supports all characters in a given string."""

    font = TTFont(font_path)
    cmap = font['cmap']

    for table in cmap.tables:
        if table.isUnicode():
            for char in characters:
                codepoint = ord(char)
                if codepoint not in table.cmap:
                    return False

    return True

def check_folder_fonts(folder_path, characters):
    """Checks TTF font files in a folder for character support."""

    for filename in os.listdir(folder_path):
        font_path = os.path.join(folder_path, filename)  # Directly assume TTF
        if not check_font_support(font_path, characters):
            print(f"Font '{filename}' does not support all characters.")
        else:
            print(f"Font '{filename}' supports all characters.")

if __name__ == "__main__":
    characters_to_test = r"""0123456789$"!#%&'()*+,-./:;<=>?@[\]^_`{|}~«»…£€¥№° —АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯЁабвгдежзийклмнопрстуфхцчшщъыьэюяёӘҒҚҢӨҰҮІҺәғқңөұүіһABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"""
    folder_to_check = "./fonts" 

    check_folder_fonts(folder_to_check, characters_to_test)
