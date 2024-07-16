import os
import random
from typing import List, Tuple

from trdg.data_generator import FakeTextDataGenerator
from trdg.utils import load_dict, load_fonts

# support RTL
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display
import logging
import traceback
import json


class GeneratorFromStrings:
    """Generator that uses a given list of strings"""

    def __init__(
            self,
            strings: List[str],
            count: int = -1,
            fonts: List[str] = [],
            out_dir: str = None,
            language: str = "en",
            sizes: List[int] = [32],
            extension: str = "jpg",
            skewing_angle: int = 0,
            random_skew: bool = False,
            blur: int = 0,
            random_blur: bool = False,
            background_types: List[int] = [0],
            distorsion_types: List[int] = [0],
            distorsion_orientation: int = 0,
            is_handwritten: bool = False,
            width: int = -1,
            alignment: int = 1,
            text_colors: List[str] = ["#282828"],
            orientation: int = 0,
            space_widths: List[float] = [1.0],
            character_spacings: List[int] = [0],
            margins: List[Tuple[int, int, int, int]] = [(5, 5, 5, 5)],
            fit: bool = False,
            output_mask: bool = False,
            word_split: bool = False,
            image_dir: str = os.path.join(
                "..", os.path.split(os.path.realpath(__file__))[0], "images"
            ),
            stroke_widths: List[int] = [0],
            stroke_fills: List[str] = ["#282828"],
            image_mode: str = "RGB",
            output_bboxes: int = 0,
            rtl: bool = False,
            random_case: bool = False,
    ):
        self.count = count
        self.strings = strings
        self.fonts = fonts
        self.extension = extension
        if len(fonts) == 0:
            self.fonts = load_fonts(language)
        self.rtl = rtl
        self.orig_strings = []
        if self.rtl:
            if language == "ckb":
                ar_reshaper_config = {
                    "delete_harakat": True, "language": "Kurdish"}
            else:
                ar_reshaper_config = {"delete_harakat": False}
            self.rtl_shaper = ArabicReshaper(configuration=ar_reshaper_config)
            # save a backup of the original strings before arabic-reshaping
            self.orig_strings = self.strings
            # reshape the strings
            self.strings = self.reshape_rtl(self.strings, self.rtl_shaper)
        self.language = language
        self.sizes = sizes
        self.out_dir = out_dir
        self.skewing_angle = skewing_angle
        self.random_skew = random_skew
        self.blur = blur
        self.random_blur = random_blur
        self.background_types = background_types
        self.distorsion_types = distorsion_types
        self.distorsion_orientation = distorsion_orientation
        self.is_handwritten = is_handwritten
        self.width = width
        self.alignment = alignment
        self.text_colors = text_colors
        self.orientation = orientation
        self.space_widths = space_widths
        self.character_spacings = character_spacings
        self.margins = margins
        self.fit = fit
        self.output_mask = output_mask
        self.word_split = word_split
        self.image_dir = image_dir
        self.output_bboxes = output_bboxes
        self.generated_count = 0
        self.stroke_widths = stroke_widths
        self.stroke_fills = stroke_fills
        self.image_mode = image_mode
        self.random_case = random_case

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        # if self.generated_count == self.count:
        #     raise StopIteration
        self.generated_count += 1
        next_string = self.orig_strings[(self.generated_count - 1) % len(self.orig_strings)] if self.rtl else \
            self.strings[(self.generated_count - 1) % len(self.strings)]
        if self.random_case:
            if random.randint(0, 1) == 0:
                next_string = next_string.capitalize()
        # Create a dictionary with all the parameters
        params = {
            "index": self.generated_count,
            "text": next_string,
            "font": random.choice(self.fonts),
            "out_dir": self.out_dir,
            "size": random.choice(self.sizes),
            "extension": self.extension,
            "skewing_angle": self.skewing_angle,
            "random_skew": self.random_skew,
            "blur": self.blur,
            "random_blur": self.random_blur,
            "background_type": random.choice(self.background_types),
            "distorsion_type": random.choice(self.distorsion_types),
            "distorsion_orientation": self.distorsion_orientation,
            "is_handwritten": self.is_handwritten,
            "name_format": 0,
            "width": self.width,
            "alignment": self.alignment,
            "text_color": random.choice(self.text_colors),
            "orientation": self.orientation,
            "space_width": random.choice(self.space_widths),
            "character_spacing": random.choice(self.character_spacings),
            "margins": random.choice(self.margins),
            "fit": random.choice([True, False]),
            "output_mask": self.output_mask,
            "word_split": self.word_split,
            "image_dir": self.image_dir,
            "stroke_width": random.choice(self.stroke_widths),
            "stroke_fill": random.choice(self.stroke_fills),
            "image_mode": self.image_mode,
            "output_bboxes": self.output_bboxes,
        }
        try:
            img = FakeTextDataGenerator.generate(
                **params
            )
        except Exception as e:
            logging.error(f"Error generating image: {e}, \n\n params: {json.dumps(params, indent=4, ensure_ascii=False)}\n\n")
            logging.error(traceback.format_exc())
            return (
                None,
                next_string,
            )
        return (
            img,
            next_string,
        )

    def reshape_rtl(self, strings: list, rtl_shaper: ArabicReshaper):
        # reshape RTL characters before generating any image
        rtl_strings = []
        for string in strings:
            reshaped_string = rtl_shaper.reshape(string)
            rtl_strings.append(get_display(reshaped_string))
        return rtl_strings


if __name__ == "__main__":
    from trdg.generators.from_wikipedia import GeneratorFromWikipedia

    s = GeneratorFromWikipedia("test")
    next(s)
