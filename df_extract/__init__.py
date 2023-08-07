import os


class Base:

    def __init__(
            self,
            file_path: str,
            output_dir: str = None,
            *args,
            **kwargs
    ):
        self.file_path = file_path
        self.name = self.file_path.split('/')[-1]
        self.output_dir = output_dir
        if not self.output_dir:
            self.output_dir = '/'.join(self.file_path.split('/')[:-1])

        self._output = f'{self.output_dir}/{self.name}.txt'
        self._output_json = f'{self.output_dir}/{self.name}.json'

    async def remove_existing_output(self) -> None:
        if os.path.exists(self._output):
            os.remove(self._output)

    async def remove_existing_json_output(self) -> None:
        if os.path.exists(self._output_json):
            os.remove(self._output_json)
