import json

import aiofiles

from aiocsv import AsyncReader, AsyncDictReader

from df_extract.base import BaseExtract
from df_extract.utils import sync_to_async


class ExtractCSV(BaseExtract):

    async def extract_as_text(self, csv_fobj):
        text = ""
        async for row in AsyncReader(csv_fobj):
            text = ''.join(row) + "\n"

        async with aiofiles.open(self._output, 'w') as fobj:
            await fobj.write(text)

    async def extract_as_json(self, csv_fobj):
        data = []
        _row = 1
        async for row in AsyncDictReader(csv_fobj):
            data.append({
                'number': _row,
                'content': await sync_to_async(json.dumps, row),
                'name': self.name
            })
            _row += 1

        async with aiofiles.open(self._output_json, 'w') as fobj:
            await fobj.write(await sync_to_async(json.dumps, data, indent=4))

    async def extract(
            self, as_json: bool = False
    ) -> None:
        print(f'Extracting => {self.file_path}')
        async with aiofiles.open(self.file_path, mode='r') as fobj:
            if not as_json:
                await self.extract_as_text(fobj)
            else:
                await self.extract_as_json(fobj)
        print(f'Extracted => {self.file_path}')
