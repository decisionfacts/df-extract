import json
import os

import aiofiles

from df_extract.utils import sync_to_async


class Base:
    """
    Base class for DF Extraction
    """

    def __init__(
            self,
            file_path: str,
            output_dir: str = None
    ):
        """
        Base class constructor for DF Extraction

        :param file_path: Valid file path as string
        :param output_dir: Valid directory path as string. Default `None`
        """
        self.file_path = file_path
        self.name = self.file_path.split('/')[-1]
        self.output_dir = output_dir
        if not self.output_dir:
            self.output_dir = '/'.join(self.file_path.split('/')[:-1])

        self._output = f'{self.output_dir}/{self.name}.txt'
        self._output_json = f'{self.output_dir}/{self.name}.json'

    async def remove_existing_output(self) -> None:
        """
        Method used to remove existing txt output if present
        """
        if os.path.exists(self._output):
            os.remove(self._output)

    async def remove_existing_json_output(self) -> None:
        """
        Method used to remove existing json output if present
        """
        if os.path.exists(self._output_json):
            os.remove(self._output_json)

    async def _write_text_output(self, text):
        async with aiofiles.open(self._output, 'w') as fobj:
            await fobj.write(text)

    async def _write_json_output(self, data):
        async with aiofiles.open(self._output_json, 'w') as fobj:
            await fobj.write(await sync_to_async(json.dumps, data, indent=4))
