from enum import Enum


class SizeEnum(Enum):
    small = "256x256"
    medium = "512x512"
    large = "1024x1024"

    def __str__(self):
        return self.name
