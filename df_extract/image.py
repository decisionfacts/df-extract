import json
from typing import Any

import aiofiles
from easyocr import easyocr

from df_extract import Base
from df_extract.base import BaseExtract
from df_extract.utils import sync_to_async, iter_to_aiter


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


class ExtractImage(BaseExtract):

    async def extract_as_text(self):
        await self.remove_existing_output()
        data = await self.read(path=self.file_path)
        text = ''
        async for row in iter_to_aiter(data):
            text += row + "\n\n\n\n"

        async with aiofiles.open(self._output_json, 'w') as fobj:
            await fobj.write(text)

    async def extract_as_json(self):
        await self.remove_existing_json_output()
        data = await self.read(path=self.file_path)

        async with aiofiles.open(self._output_json, 'w') as fobj:
            await fobj.write(await sync_to_async(json.dumps, data, indent=4))

    async def extract(self, as_json: bool = False):
        print(f'Extracting => {self.file_path}')
        if not as_json:
            await self.extract_as_text()
        else:
            await self.extract_as_json()
        print(f'Extracted => {self.file_path}')
