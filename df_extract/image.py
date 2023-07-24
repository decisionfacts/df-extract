from typing import Any

from utils import sync_to_async
from easyocr import easyocr


class ExtractImage:

    def __init__(self, model_storage_dir: str, lang_list: list[str] | None = None):
        self._reader = easyocr.Reader(
            lang_list or ['en'],
            gpu=False,
            download_enabled=False,
            model_storage_directory=model_storage_dir,
        )

    async def extract(self, path: Any):
        try:
            return await sync_to_async(
                self._reader.readtext,
                path,
                detail=0,
                paragraph=True,
                # decoder='wordbeamsearch',
                # height_ths=100,
                # width_ths=100
                rotation_info=[90, 180, 270]
            )
        except Exception as ex:
            print(ex)
            return []
