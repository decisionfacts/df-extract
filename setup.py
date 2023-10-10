import os
from distutils.core import setup

from setuptools import find_packages


def readme():
    readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')
    with open(readme_path) as fobj:
        return fobj.read()


setup(
    name='df_extract',
    version='v0.0.1',
    description='Utils for decisionforce extract',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='DecisionForce',
    author_email='info@decisionforce.io',
    license='MIT',
    packages=find_packages(exclude=('dhl',)),
    include_package_data=True,
    install_requires=[
        'aiofiles',
        'aiopath',
        'aiocsv',
        'python-pptx',
        'python-docx',
        'easyocr',
        'pymupdf',
        'Pillow==9.5.0'
    ]
)
