from setuptools import setup, find_packages

setup(
    name='cocoa-detect',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'ultralytics',
        'Pillow',
        'shapely',
        'rasterio',
        'numpy',
        'tqdm',
        'pyproj',
    ],
    entry_points={
        'console_scripts': [
            'cocoa-detect=cocoa_cli_pipeline.cli:main',
        ],
    },
    author='Michael Ofeor',
    description='Full-stack cocoa plant detector with YOLOv8, Streamlit, GIS, and CLI support',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
