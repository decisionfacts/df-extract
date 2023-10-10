import os
from distutils.core import setup

from setuptools import find_packages


def readme():
    readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
    with open(readme_path) as fobj:
        return fobj.read()


_description = '''
DecisionFacts Extraction Library extracts content from PDF, PPTX, Docx, png, jpg., and convert as structured JSON data.
'''


setup(
    name='df_extract',
    version='v0.0.2',
    description=_description,
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Syed',
    author_email='syed@decisionfacts.io',
    maintainer='DecisionFacts',
    maintainer_email='info@decisionfacts.io',
    license='Apache License 2.0',
    url='https://github.com/decisionfacts/df-extract',
    download_url='https://github.com/decisionfacts/df-extract.git',
    keywords=['df extract content pdf pptx ppt docx doc png jpg jpeg'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'aiocsv==1.2.4',
        'aiofiles==23.1.0',
        'aiopath==0.6.11',
        'easyocr==1.7.0',
        'Pillow==9.5.0',
        'PyMuPDF==1.22.5',
        'python-pptx==0.6.21',
        'python-docx==0.8.11'
    ]
)
