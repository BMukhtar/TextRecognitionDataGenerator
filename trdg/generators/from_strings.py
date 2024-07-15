import os
import random
from typing import List, Tuple

from trdg.data_generator import FakeTextDataGenerator
from trdg.utils import load_dict, load_fonts

# support RTL
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display


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
                ar_reshaper_config = {"delete_harakat": True, "language": "Kurdish"}
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
        return (
            FakeTextDataGenerator.generate(
                self.generated_count,
                next_string,
                random.choice(self.fonts),
                self.out_dir,
                random.choice(self.sizes),
                self.extension,
                self.skewing_angle,
                self.random_skew,
                self.blur,
                self.random_blur,
                random.choice(self.background_types),
                random.choice(self.distorsion_types),
                self.distorsion_orientation,
                self.is_handwritten,
                0,
                self.width,
                self.alignment,
                random.choice(self.text_colors),
                self.orientation,
                random.choice(self.space_widths),
                random.choice(self.character_spacings),
                random.choice(self.margins),
                random.choice([True, False]),
                self.output_mask,
                self.word_split,
                self.image_dir,
                # random stroke width and fill
                random.choice(self.stroke_widths),
                random.choice(self.stroke_fills),
                self.image_mode,
                self.output_bboxes,
            ),
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
