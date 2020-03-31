from enum import Enum
from typing import AnyStr


class Biometrics:

    # bio_types = Enum('IRIS', 'FINGER', 'FACE')
    # sub_types = Enum('Left Eye', 'FINGER', 'FACE')

    def __init__(self, bio_type: AnyStr, sub_type: AnyStr, file_content: AnyStr):
        self._bio_type = bio_type
        self._sub_type = sub_type
        self._file_content = file_content

    @property
    def bio_type(self):
        return self._bio_type

    @property
    def sub_type(self):
        return self._sub_type

    @property
    def file_content(self):
        return self._file_content


