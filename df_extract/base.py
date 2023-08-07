import abc
from typing import Any

from easyocr import easyocr

from df_extract import Base
from df_extract.utils import sync_to_async


class ImageExtract:

    def __init__(
            self,
            model_download_enabled: bool = False,
            model_storage_dir: str = None,
            lang_list: list[str] | None = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._reader = easyocr.Reader(
            lang_list or ['en'],
            # gpu=False,
            download_enabled=model_download_enabled,
            model_storage_directory=model_storage_dir,
        )

    async def read(self, path: Any):
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


class BaseExtract(abc.ABC, Base):

    def __init__(
            self,
            img_extract_obj: ImageExtract | None = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._image_extract = img_extract_obj

    async def extract_image(self, image) -> str:
        if self._image_extract:
            image_data = await self._image_extract.read(path=image)
            return " ".join(image_data)

    @abc.abstractmethod
    async def extract(self, as_json: bool = False) -> None:
        pass
