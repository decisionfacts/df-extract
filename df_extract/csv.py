import json

import aiofiles

from aiocsv import AsyncReader, AsyncDictReader

from df_extract.base import BaseExtract
from df_extract.utils import sync_to_async


class ExtractCSV(BaseExtract):
    """
    Class for CSV Extraction
    """

    async def extract_as_text(self, csv_fobj):
        """
        Method to extract csv content as text

        :param csv_fobj: Valid aiofile object
        """
        text = ""
        async for row in AsyncReader(csv_fobj):
            text = ''.join(row) + "\n"

        await self._write_text_output(text=text)

    async def extract_as_json(self, csv_fobj):
        """
        Method to extract csv content as text

        :param csv_fobj: Valid aiofile object
        """
        data = []
        _row = 1
        async for row in AsyncDictReader(csv_fobj):
            data.append({
                'number': _row,
                'content': await sync_to_async(json.dumps, row),
                'name': self.name
            })
            _row += 1

        await self._write_json_output(data=data)

    async def extract(
            self, as_json: bool = False
    ) -> None:
        """
        Method to extract csv content

        :param as_json: Extracted content will be stored as json. Default `False`
        """
        print(f'Extracting => {self.file_path}')
        async with aiofiles.open(self.file_path, mode='r') as fobj:
            if not as_json:
                await self.extract_as_text(fobj)
            else:
                await self.extract_as_json(fobj)
        print(f'Extracted => {self.file_path}')
