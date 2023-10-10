from df_extract.base import BaseExtract
from df_extract.extract_util import cleanup
from df_extract.utils import iter_to_aiter


class ExtractImage(BaseExtract):
    """
    Class for Image Extraction
    """

    async def extract_as_text(self):
        """
        Method to extract image content as text
        """
        await self.remove_existing_output()
        data = await self._image_extract.read(path=self.file_path)
        text = ''
        async for row in iter_to_aiter(data):
            text += row + "\n\n\n\n"
        cleaned_up_data = await cleanup(text)
        await self._write_text_output(text=cleaned_up_data)

    async def extract_as_json(self):
        """
        Method to extract image content as json
        """
        await self.remove_existing_json_output()
        page_data = await self._image_extract.read(path=self.file_path)
        cleaned_up_data = await cleanup(page_data)
        data = [{
            'number': 1,
            'content': cleaned_up_data,
            'name': self.name
        }]

        await self._write_json_output(data=data)

    async def extract(self, as_json: bool = False):
        """
        Method to extract image content

        :param as_json: Extracted content will be stored as json. Default `False`
        """
        print(f'Extracting => {self.file_path}')
        if not as_json:
            await self.extract_as_text()
        else:
            await self.extract_as_json()
        print(f'Extracted => {self.file_path}')
