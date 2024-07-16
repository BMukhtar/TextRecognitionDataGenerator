import sys
sys.path.insert(0, '..')
import os
from PIL import Image
from trdg.data_generator import FakeTextDataGenerator

# root 
root = os.path.dirname(os.path.abspath(__file__))

margin_max = 3

params = {
    "index": 390,
    "text": "–",
    "font": "./fonts/Caveat-Medium.ttf",
    "out_dir": None,
    "size": 29,
    "extension": "jpg",
    "skewing_angle": 10,
    "random_skew": True,
    "blur": 1,
    "random_blur": True,
    "background_type": 2,
    "distorsion_type": 0,
    "distorsion_orientation": 0,
    "is_handwritten": False,
    "name_format": 0,
    "width": -1,
    "alignment": 0,
    "text_color": "#999999",
    "orientation": 0,
    "space_width": 1.0,
    "character_spacing": 3,
    "margins": [ #  "margins": (margin_max, margin_max, margin_max, margin_max),
        2,
        3,
        3,
        0
    ],
    "fit": True,
    "output_mask": False,
    "word_split": False,
    "image_dir": "./backgrounds",
    "stroke_width": 0,
    "stroke_fill": "#999999",
    "image_mode": "RGB",
    "output_bboxes": 0
}

font_path = os.path.join(root, params['font'])
params['font'] = font_path

# Function to generate a sample image
def generate_sample_image(index):
    return FakeTextDataGenerator.generate(**params)

# Generate and display the sample image
img = generate_sample_image(0)
img.save("./sample_image.jpg")