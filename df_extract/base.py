import abc
import os

from df_extract.image import ExtractImage


class BaseExtract(abc.ABC):

    def __init__(
            self,
            file_path: str,
            img_extract_obj: ExtractImage | None = None,
    ):
        self.file_path = file_path
        self.name = self.file_path.split('/')[-1]
        self._image_extract = img_extract_obj
        self._output = f'{self.file_path}.txt'
        self._output_json = f'{self.file_path}.json'

    async def remove_existing_output(self) -> None:
        if os.path.exists(self._output):
            os.remove(self._output)

    async def remove_existing_json_output(self) -> None:
        if os.path.exists(self._output_json):
            os.remove(self._output_json)

    async def extract_image(self, image) -> str:
        if self._image_extract:
            image_data = await self._image_extract.extract(path=image)
            return " ".join(image_data)

    @abc.abstractmethod
    async def extract(self, as_json: bool = False) -> None:
        pass
