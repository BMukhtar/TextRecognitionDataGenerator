import requests
import os
import re

def get_urls_and_names(content):
    font_data = []
    font_family_pattern = re.compile(r'font-family:\s*\'(.+?)\'')
    url_pattern = re.compile(r'url\((https:\/\/.+?)\)')
    
    font_families = font_family_pattern.findall(content)
    urls = url_pattern.findall(content)
    
    for family, url in zip(font_families, urls):
        font_data.append((family, url))
    
    return font_data

def fetch_data(font_data):
    if not os.path.exists('dfonts'):
        os.mkdir('dfonts')
    
    for index, (font_name, url) in enumerate(font_data):
        response = requests.get(url)
        if response.status_code == 200:
            # Clean the font name to use as a filename
            clean_name = re.sub(r'[^\w\-_\. ]', '_', font_name)
            filename = f"{clean_name}.ttf"
            
            with open(f'dfonts/{filename}', 'wb') as f:
                f.write(response.content)
            print(f'Downloaded {filename}, {index + 1} of {len(font_data)} fonts.')
        else:
            print(f'Failed to download {font_name}')

def main(method, src):
    if method == 'file':
        with open(src, 'r') as f:
            content = f.read()
    elif method == 'link':
        response = requests.get(src)
        content = response.text
    else:
        print("Invalid method. Use 'file' or 'link'.")
        return

    font_data = get_urls_and_names(content)
    print(f'Fetched {len(font_data)} fonts.')
    fetch_data(font_data)

if __name__ == "__main__":
    fonts = [
        "Times New Roman",
        "Cambria",
        "Georgia",
        "Garamond",
        "Merriweather",
        "Libre Baskerville",
        "Bodoni",
        "Lora",
        "Playfair Display",
        "Ramaraja",
        "Century Schoolbook"
    ]
    
    # Construct Google Fonts URL
    fonts_string = "|".join(font.replace(" ", "+") for font in fonts)
    google_fonts_url = f"https://fonts.googleapis.com/css?family={fonts_string}&display=swap"
    
    main(method='link', src=google_fonts_url)