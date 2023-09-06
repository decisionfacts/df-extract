import asyncio
import json
import re

from aiopath import AsyncPath

from df_extract import sync_to_async
from df_extract.utils import iter_to_aiter

SPACE_REGEX = re.compile(r'( ){2,}')
MULTI_LINE_REGEX = re.compile(r"(\n){2,}")
DOUBLE_QUOTES_REGEX = re.compile(r'\"')
ASCII_REGEX = re.compile(r'[^\x00-\x7f]+')


async def read_data(path: AsyncPath) -> list | dict:
    async with path.open(mode='r') as fobj:
        f_data = await fobj.read()
        return await sync_to_async(json.loads, f_data)


async def cleanup_spaces(content: str) -> str:
    return SPACE_REGEX.sub("  ", content)


async def cleanup_multi_line(content: str) -> str:
    return MULTI_LINE_REGEX.sub("\n\n", content)


async def cleanup_double_quotes(content: str) -> str:
    return DOUBLE_QUOTES_REGEX.sub("'", content)


async def cleanup_ascii(content: str) -> str:
    return ASCII_REGEX.sub("", content)


async def cleanup(content: str) -> str:
    content = content.encode().decode('unicode_escape')
    res = await cleanup_spaces(content)
    res = await cleanup_multi_line(res)
    res = await cleanup_double_quotes(res)
    res = await cleanup_ascii(res)
    return res


async def cleanup_from_file(file_path: str, output_dir: str | None = None):
    path = AsyncPath(file_path)
    data = await read_data(path)
    async for item in iter_to_aiter(data):
        content = item.get('content')
        if content:
            res = await cleanup(content)
            item['content'] = res

    output_file_name = path.name
    if output_dir:
        output_file_name = AsyncPath(output_dir) / output_file_name
    else:
        output_file_name = AsyncPath(file_path + ".json")
    async with output_file_name.open(mode='w') as fobj:
        data = await sync_to_async(json.dumps, data, indent=4)
        await fobj.write(data)


if __name__ == '__main__':
    asyncio.run(
        cleanup_from_file(
            file_path='',
            output_dir=''
        )
    )
