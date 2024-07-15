import os
from typing import List, Tuple

from trdg.generators.from_strings import GeneratorFromStrings
from trdg.data_generator import FakeTextDataGenerator
from trdg.string_generator import create_strings_from_dict
from trdg.utils import load_dict, load_fonts


class GeneratorFromDict:
    """Generator that uses words taken from pre-packaged dictionaries"""

    def __init__(
        self,
        count: int = -1,
        length: int = 1,
        allow_variable: bool = False,
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
        path: str = "",
        rtl: bool = False,
        random_case: bool = False,
    ):
        self.count = count
        self.length = length
        self.allow_variable = allow_variable

        if path == "":
            self.dict = load_dict(
                os.path.join(
                    os.path.dirname(__file__), "..", "dicts", language + ".txt"
                )
            )
        else:
            self.dict = load_dict(path)

        self.batch_size = min(max(count, 1), 1000)
        self.steps_until_regeneration = self.batch_size

        self.generator = GeneratorFromStrings(
            create_strings_from_dict(
                self.length, self.allow_variable, self.batch_size, self.dict
            ),
            count,
            fonts if len(fonts) else load_fonts(language),
            out_dir,
            language,
            sizes,
            extension,
            skewing_angle,
            random_skew,
            blur,
            random_blur,
            background_types,
            distorsion_types,
            distorsion_orientation,
            is_handwritten,
            width,
            alignment,
            text_colors,
            orientation,
            space_widths,
            character_spacings,
            margins,
            fit,
            output_mask,
            word_split,
            image_dir,
            stroke_widths,
            stroke_fills,
            image_mode,
            output_bboxes,
            rtl,
            random_case,
        )

    def __iter__(self):
        return self.generator

    def __next__(self):
        return self.next()

    def next(self):
        if self.generator.generated_count >= self.steps_until_regeneration:
            self.generator.strings = create_strings_from_dict(
                self.length, self.allow_variable, self.batch_size, self.dict
            )
            self.steps_until_regeneration += self.batch_size
        return self.generator.next()
