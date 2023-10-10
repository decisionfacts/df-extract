import abc
from typing import Any

from easyocr import easyocr

from df_extract import Base
from df_extract.utils import sync_to_async


class ImageExtract:
    """
    Base Image Extract class
    """

    def __init__(
            self,
            model_download_enabled: bool = False,
            model_storage_dir: str = None,
            lang_list: list[str] | None = None,
    ):
        """
        Base Image Extract class constructor

        :param model_download_enabled: Download model from the internet. Default `False`
        :param model_storage_dir: Valid directory path for downloaded models. Default `None`
        :param lang_list: List contains langauge strings. Default `['en']`
        """
        self._reader = easyocr.Reader(
            lang_list or ['en'],
            # gpu=False,
            download_enabled=model_download_enabled,
            model_storage_directory=model_storage_dir,
        )

    async def read(self, path: Any):
        """
        Method to read and extract content from given image path

        :param path: Valid image file path or stream
        :return: List of extracted content as string
        """
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
    """
    Base class for Extraction
    """

    def __init__(
            self,
            img_extract_obj: ImageExtract | None = None,
            *args,
            **kwargs
    ):
        """
        Base class constructor for Extraction

        :param img_extract_obj: `ImageExtract` object. Default `None`
        :param args: parent class arguments
        :param kwargs: parent class keyword arguments
        """
        super().__init__(*args, **kwargs)
        self._image_extract = img_extract_obj

    async def extract_image(self, image) -> str:
        """
        Method to extract image from the given image object

        :param image: `Image` object
        :return: Extracted content as string
        """
        if self._image_extract:
            image_data = await self._image_extract.read(path=image)
            return " ".join(image_data)

    @abc.abstractmethod
    async def extract_as_text(self, *args, **kwargs):
        """
        Abstract method, should implement in the all child classes

        :param args: arguments for implementation
        :param kwargs: keyword arguments for implementation
        """
        pass

    @abc.abstractmethod
    async def extract_as_json(self, *args, **kwargs):
        """
        Abstract method, should implement in the all child classes

        :param args: arguments for implementation
        :param kwargs: keyword arguments for implementation
        """
        pass

    @abc.abstractmethod
    async def extract(self, as_json: bool = False) -> None:
        """
        Abstract method, should implement in the all child classes

        :param as_json: Value as `bool`. Default `False`
        """
        pass
