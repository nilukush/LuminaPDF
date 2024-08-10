from setuptools import setup, find_packages

setup(
    name="pdf_scanner",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt6',
        'click',
        'PyPDF2',
    ],
    entry_points={
        'console_scripts': [
            'pdf_scanner=src.main:main',
        ],
    },
)
