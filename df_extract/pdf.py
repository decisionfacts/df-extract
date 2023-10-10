import json

import fitz
from fitz import Document

from df_extract.base import BaseExtract
from df_extract.extract_util import cleanup
from df_extract.utils import iter_to_aiter, sync_to_async


class ExtractPDF(BaseExtract):
    """
    Class for PDF Extraction
    """

    def __init__(self, *args, **kwargs):
        """
        PDF Extract class constructor

        :param args: Base class arguments
        :param kwargs: Base class keyword arguments
        """
        super().__init__(*args, **kwargs)
        self._convert_as_image: bool = False

    async def _extract_images(self, images, doc):
        image_data = ""
        async for image in iter_to_aiter(images):
            if image and image[0]:
                xref_img = doc.extract_image(image[0])
                if xref_img:
                    try:
                        image_data = await self.extract_image(xref_img['image'])
                        if image_data:
                            image_data += await sync_to_async(json.dumps, image_data) + "\n\n"
                    except AttributeError as ex:
                        print(ex)
        return image_data

    async def _extract_page_data(self, page, doc) -> str:
        page_data = page.get_text()
        _images = page.get_images()
        page_data += await self._extract_images(_images, doc)
        cleaned_up_data = await cleanup(page_data)
        return cleaned_up_data

    async def _extract_page_as_image(
            self,
            page,
            zoom_x: float = 2.0,
            zoom_y: float = 2.0
    ) -> str:
        page_data = ''
        mat = fitz.Matrix(zoom_x, zoom_y)
        _pix_map = page.get_pixmap(matrix=mat)
        _result = await self.extract_image(_pix_map.tobytes(output='jpg'))
        if _result:
            page_data += '\n'.join(_result)
        cleaned_up_data = await cleanup(page_data)
        return cleaned_up_data

    async def extract_as_text(self, doc: Document):
        """
        Method to extract PDF content as text

        :param doc: Valid `fitz.Document` object
        """
        await self.remove_existing_output()
        text = ""
        apages = iter_to_aiter(doc)
        if not self._convert_as_image:
            async for page in apages:
                text += await self._extract_page_data(page, doc)
                text += "\n\n\n\n"
        else:
            async for page in apages:
                text += await self._extract_page_as_image(page)
                text += "\n\n\n\n"

        await self._write_text_output(text=text)

    async def extract_as_json(self, doc: Document):
        """
        Method to extract PDF content as json

        :param doc: Valid `fitz.Document` object
        """
        await self.remove_existing_json_output()
        data = []
        apages = iter_to_aiter(doc)
        if not self._convert_as_image:
            async for page in apages:
                page_data = await self._extract_page_data(page, doc)
                page_content = {
                    'number': page.number + 1,
                    'content': page_data,
                    'name': self.name
                }
                data.append(page_content)
        else:
            async for page in apages:
                page_data = await self._extract_page_as_image(page)
                page_content = {
                    'number': page.number + 1,
                    'content': page_data,
                    'name': self.name
                }
                data.append(page_content)

        await self._write_json_output(data=data)

    async def extract(self, as_json: bool = False, convert_as_image: bool = False) -> None:
        """
        Method to extract PDF content

        :param as_json: Extracted content will be stored as json. Default `False`
        :param convert_as_image: Special option to convert PDF page as image and extract. Default `False`
        """
        self._convert_as_image = convert_as_image
        print(f'Extracting => {self.file_path}')
        with fitz.Document(self.file_path) as doc:
            if not as_json:
                await self.extract_as_text(doc)
            else:
                await self.extract_as_json(doc)
        print(f'Extracted => {self.file_path}')
