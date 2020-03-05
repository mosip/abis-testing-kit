from enum import Enum
from typing import AnyStr


class Biometrics:

    bio_types = Enum('IRIS', 'FINGER', 'FACE')

    def __init__(self, bio_type: bio_types, file_content: AnyStr):
        self.bio_type = bio_type
        self.file_content = file_content
