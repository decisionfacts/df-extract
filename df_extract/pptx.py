import json

import aiofiles
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

from base import BaseExtract
from utils import iter_to_aiter, sync_to_async


class ExtractPPTx(BaseExtract):

    @staticmethod
    async def __extract_table(table):
        table_data = []
        async for _row in iter_to_aiter(table.rows):
            row_cols = []
            async for _cell in iter_to_aiter(_row.cells):
                row_cols.append(_cell.text)
            table_data.append(row_cols)
        return table_data

    @staticmethod
    async def __extract_text(text_frame):
        _paragraph = ""
        async for paragraph in iter_to_aiter(text_frame.paragraphs):
            async for run in iter_to_aiter(paragraph.runs):
                _paragraph += run.text
        return _paragraph

    async def _extract_shape(self, shape) -> str:
        text = ""
        _shape_type = shape.shape_type
        if _shape_type == MSO_SHAPE_TYPE.GROUP:
            _g_text = ""
            async for _shape in iter_to_aiter(shape.shapes):
                _g_text += await self._extract_shape(_shape)
            text += _g_text
        elif _shape_type == MSO_SHAPE_TYPE.PICTURE:
            if self._image_extract:
                try:
                    image_date = await self.extract_image(shape.image.blob)
                    if image_date:
                        text += json.dumps(image_date) + "\n\n"
                except AttributeError as ex:
                    print(ex)
        elif _shape_type == MSO_SHAPE_TYPE.CHART:
            pass
        elif _shape_type == MSO_SHAPE_TYPE.TABLE:
            table_data = await self.__extract_table(shape.table)
            text += json.dumps(table_data) + "\n\n"
        else:
            if shape.has_text_frame:
                # print("Shap Type => ", _shape.shape_type)
                # paragraph = ""
                # async for _paragraph in iter_to_aiter(_shape.text_frame.paragraphs):
                #     paragraph += _paragraph.text
                # print(paragraph)
                # paragraph = await self.extract_text(_shape.text_frame)
                # text += paragraph + "\n\n"
                text += shape.text + "\n\n"
        return text

    async def _extract_shapes(self, shapes):
        shapes_data = ""
        async for _shape in iter_to_aiter(shapes):
            _shape_type = _shape.shape_type
            if _shape.has_chart:
                pass
            if _shape.has_text_frame:
                pass
            if _shape.has_table:
                pass
            shapes_data += await self._extract_shape(_shape)
        return shapes_data

    async def extract_as_text(self, presentation):
        await self.remove_existing_output()
        text = ""
        async for _slide in iter_to_aiter(presentation.slides):
            text += await self._extract_shapes(_slide.shapes)
            text += "\n\n\n\n"

        async with aiofiles.open(self._output, 'w') as fobj:
            await fobj.write(text)

    async def extract_as_json(self, presentation):
        await self.remove_existing_json_output()
        data = []
        slide_no = 1
        async for _slide in iter_to_aiter(presentation.slides):
            page_data = await self._extract_shapes(_slide.shapes)
            page_content = {
                'number': slide_no,
                'content': page_data,
                'name': self.name
            }
            data.append(page_content)
            slide_no += 1

        # print(data)
        async with aiofiles.open(self._output_json, 'w') as fobj:
            await fobj.write(await sync_to_async(json.dumps, data, indent=4))

    async def extract(self, as_json: bool = False, save_output: bool = False):
        print(f'Extracting => {self.file_path}')
        presentation = Presentation(pptx=self.file_path)
        if not as_json:
            await self.extract_as_text(presentation)
        else:
            await self.extract_as_json(presentation)
        print(f'Extracted => {self.file_path}')
