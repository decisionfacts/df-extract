import json

import aiofiles

from df_extract.base import BaseExtract
from df_extract.utils import sync_to_async, iter_to_aiter


class ExtractImage(BaseExtract):

    async def extract_as_text(self):
        await self.remove_existing_output()
        data = await self._image_extract.read(path=self.file_path)
        text = ''
        async for row in iter_to_aiter(data):
            text += row + "\n\n\n\n"

        async with aiofiles.open(self._output_json, 'w') as fobj:
            await fobj.write(text)

    async def extract_as_json(self):
        await self.remove_existing_json_output()
        data = await self._image_extract.read(path=self.file_path)

        async with aiofiles.open(self._output_json, 'w') as fobj:
            await fobj.write(await sync_to_async(json.dumps, data, indent=4))

    async def extract(self, as_json: bool = False):
        print(f'Extracting => {self.file_path}')
        if not as_json:
            await self.extract_as_text()
        else:
            await self.extract_as_json()
        print(f'Extracted => {self.file_path}')
