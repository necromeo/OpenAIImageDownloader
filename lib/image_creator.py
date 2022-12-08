import base64
import logging
from io import BytesIO
from os import getenv, sep
from pathlib import Path
from typing import Dict, List

import openai
from dotenv import load_dotenv
from PIL import Image

from .enums import SizeEnum

load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)


class OpenAiImageCreator:
    """
    Class with methods to request and save images requested to OpenAI.
    """

    def __init__(self, prompt: str, size: SizeEnum, variations: int):
        self.prompt = prompt
        self.size = size.value
        self.variations = variations

    def _request_image(self) -> Dict[str, str | List[Dict[str, str]]] | None:
        """
        Requests the image cration to OpenAi.
        """
        openai.api_key = getenv("OPENAI_KEY")
        logging.info("Creating image/s...")
        try:
            return openai.Image.create(
                prompt=self.prompt,
                n=self.variations,
                size=self.size,
                response_format="b64_json",
            )

        except Exception as e:
            logging.error("Image creation failed!")
            logging.error(str(e))
            return

    def underscore_prompt(self):
        """Turns the prompt input into a lowercase, no space
        string.
        """
        return self.prompt.replace(" ", "_").lower()

    def _save(
        self,
        save_path: Path,
        previous_contents: List[str],
        img_payload: str,
    ):
        """
        Private method to iterate through the created images and save them
        to disk.
        """
        for idx, enc_img in enumerate(img_payload, start=1):
            logging.info(f"Saving image {idx}")
            actual_img = Image.open(BytesIO(base64.b64decode(enc_img)))

            file_name = f"{save_path}{sep}{self.underscore_prompt()}_{idx}"

            if f"{file_name}.jpg" in previous_contents:
                actual_img.save(f"{file_name}_1.jpg")  # TODO improve
                return

            actual_img.save(f"{file_name}.jpg")
        logging.info("Job finished!")

    def _create_save_folder(self) -> Path:
        """
        Creates the export folder if it doesn't exist.
        """
        p = Path(f".{sep}export")
        p.mkdir(exist_ok=True)
        return p

    def save_image(self):
        """
        Saves the prompted image/s.
        """
        if image := self._request_image():
            save_path = self._create_save_folder()
            previous_contents = [str(c) for c in save_path.iterdir() if c.is_file()]

            logging.info("Writing image/s to disk...")
            img_data: List[Dict[str, str]] = image.get("data", [])

            img_payload: str = [data.get("b64_json") for data in img_data]

            return self._save(save_path, previous_contents, img_payload)
