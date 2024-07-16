import sys
sys.path.insert(0, '..')
import os
from PIL import Image
from trdg.data_generator import FakeTextDataGenerator

margin_max = 3
# Fixed configuration
config = {
    "font": "./fonts/Alice-Regular.ttf",
    "size": 20,
    "background_type": 0,  # 0: Gaussian noise
    "distorsion_type": 3,  # 1: Sin wave
    "text_color": "#000000",
    "space_width": 1,
    "character_spacing": 0,
    "margins": (margin_max, margin_max, margin_max, margin_max),
    "stroke_width": 1,
    "stroke_fill": "#0000ff",
}

# Function to generate a sample image
def generate_sample_image(index):
    return FakeTextDataGenerator.generate(
        index=index,
        text=f"",
        font=config["font"],
        out_dir=None,
        size=config["size"],
        extension="jpg",
        skewing_angle=10,
        random_skew=False,
        blur=1,
        random_blur=False,
        background_type=config["background_type"],
        distorsion_type=config["distorsion_type"],
        distorsion_orientation=0,
        is_handwritten=False,
        name_format=0,
        width=-1,
        alignment=0,
        text_color=config["text_color"],
        orientation=0,
        space_width=config["space_width"],
        character_spacing=config["character_spacing"],
        margins=config["margins"],
        fit=True,
        output_mask=True,
        word_split=False,
        image_dir=None,
        stroke_width=config["stroke_width"],
        stroke_fill=config["stroke_fill"],
        image_mode="RGB",
        output_bboxes=1
    )

# Generate and display the sample image
img, label = generate_sample_image(0)
img.save("./sample_image.jpg")

# Print the configuration used
print("\nConfiguration used:")
for key, value in config.items():
    print(f"{key}: {value}")