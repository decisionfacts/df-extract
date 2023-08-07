from docx import Document

from df_extract.base import BaseExtract
from df_extract.utils import iter_to_aiter


class ExtractDocx(BaseExtract):

    async def extract_as_text(self, doc: Document):
        await self.remove_existing_output()
        text = ''
        async for para in iter_to_aiter(doc.paragraphs):
            text += para.text + '\n\n\n\n'

        await self._write_text_output(text=text)

    async def extract_as_json(self, doc: Document):
        await self.remove_existing_json_output()
        data = []
        _para_count = 1
        async for para in iter_to_aiter(doc.paragraphs):
            para_content = {
                'number': _para_count,
                'content': para.text,
                'name': self.name
            }
            data.append(para_content)
            _para_count += 1

        await self._write_json_output(data=data)

    async def extract(self, as_json: bool = False) -> None:
        print(f'Extracting => {self.file_path}')
        doc = Document(self.file_path)
        if not as_json:
            await self.extract_as_text(doc)
        else:
            await self.extract_as_json(doc)
        print(f'Extracted => {self.file_path}')
