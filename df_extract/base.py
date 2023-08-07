import abc

from df_extract import Base
from df_extract.image import ExtractImage


class BaseExtract(abc.ABC, Base):

    def __init__(
            self,
            img_extract_obj: ExtractImage | None = None,
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
