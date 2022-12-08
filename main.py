import argparse

from lib.enums import SizeEnum
from lib.image_creator import OpenAiImageCreator

parser = argparse.ArgumentParser()
parser.add_argument(
    "prompt",
    help="The text prompt for the image creation.",
    type=str,
)
parser.add_argument(
    "-s",
    "--size",
    help="The size of the exported image/s",
    type=SizeEnum,
    choices=list(SizeEnum),
    default=SizeEnum.medium.value,
)
parser.add_argument(
    "-n",
    "--variations",
    help="How many images should be created. Can be up to 10",
    type=int,
    default=1,
)
args = parser.parse_args()

if __name__ == "__main__":

    image_prompt = OpenAiImageCreator(args.prompt, args.size, args.variations)
    image_prompt.save_image()
