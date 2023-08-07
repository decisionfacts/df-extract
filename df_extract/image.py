from df_extract.base import BaseExtract
from df_extract.utils import iter_to_aiter


class ExtractImage(BaseExtract):

    async def extract_as_text(self):
        await self.remove_existing_output()
        data = await self._image_extract.read(path=self.file_path)
        text = ''
        async for row in iter_to_aiter(data):
            text += row + "\n\n\n\n"

        await self._write_text_output(text=text)

    async def extract_as_json(self):
        await self.remove_existing_json_output()
        data = await self._image_extract.read(path=self.file_path)

        await self._write_json_output(data=data)

    async def extract(self, as_json: bool = False):
        print(f'Extracting => {self.file_path}')
        if not as_json:
            await self.extract_as_text()
        else:
            await self.extract_as_json()
        print(f'Extracted => {self.file_path}')
