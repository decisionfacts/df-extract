
# DF Extract Lib

[![PyPI version](https://badge.fury.io/py/df-extract.svg)](https://badge.fury.io/py/df-extract) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Requirements

Python 3.10+

## Installation

```shell
# Using pip
$ python -m pip install df-extract

# Manual install
$ python -m pip install .
```

### 1. To extract content from `PDF`

```python
from df_extract.pdf import ExtractPDF


path = "/home/test/ABC.pdf"

extract_pdf = ExtractPDF(file_path=path)

# By default, output as text
extract_pdf.extract()  # Output will be located `/home/test/ABC.pdf.txt`

# Output as json
extract_pdf.extract(as_json=True)  # Output will be located `/home/test/ABC.pdf.json`
```

> You can change the output directory with simply pass `output_dir` param
```python
from df_extract.pdf import ExtractPDF


path = "/home/test/ABC.pdf"

extract_pdf = ExtractPDF(file_path=path, output_dir="/home/test/output")
extract_pdf.extract()
```

#### Extract content from `PDF` with image data
> This requires [`easyocr`](https://github.com/jaidedai/easyocr)

```python
from df_extract.base import ImageExtract
from df_extract.pdf import ExtractPDF


path = "/home/test/ABC.pdf"

image_extract = ImageExtract(model_download_enabled=True)
extract_pdf = ExtractPDF(file_path=path, image_extract=image_extract)
extract_pdf.extract()
```

### 2. To extract content from `PPT` and `PPTx`

```python
from df_extract.pptx import ExtractPPTx


path = "/home/test/DEF.pptx"

extract_pptx = ExtractPPTx(file_path=path)

# By default, output as text
extract_pptx.extract()  # Output will be located `/home/test/DEF.pptx.txt`

# Output as json
extract_pptx.extract(as_json=True)  # Output will be located `/home/test/DEF.pptx.json`
```

### 3. To extract content from `Doc` and `Docx`

```python
from df_extract.docx import ExtractDocx


path = "/home/test/GHI.docx"

extract_docx = ExtractDocx(file_path=path)

# By default, output as text
extract_docx.extract()  # Output will be located `/home/test/GHI.docx.txt`

# Output as json
extract_docx.extract(as_json=True)  # Output will be located `/home/test/GHI.docx.json`
```

### 4. To extract content from `PNG`, `JPEG` and `JPG`

```python
from df_extract.image import ExtractImage


path = "/home/test/JKL.png"

extract_png = ExtractImage(file_path=path)

# By default, output as text
extract_png.extract()  # Output will be located `/home/test/JKL.png.txt`

# Output as json
extract_png.extract(as_json=True)  # Output will be located `/home/test/JKL.png.json`
```