import os
import requests
from urllib.parse import quote

def download_font(font_name):
    base_url = "https://fonts.google.com/download?family="
    encoded_name = quote(font_name)
    url = f"{base_url}{encoded_name}"
    
    response = requests.get(url)
    if response.status_code == 200:
        filename = f"{font_name.replace(' ', '_')}.zip"
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {font_name}")

def main():
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

    for font in fonts:
        download_font(font)

if __name__ == "__main__":
    main()