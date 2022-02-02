import setuptools
from prettyjson.version import __version__

with open("readme.md", 'r') as ld:
    long_description = ld.read()

setuptools.setup(
    name='prettyjson',
    version=__version__,
    author='Jaylen A. Douglas',
    description="Pretty Print Json",
    long_description=long_description,
    packages=['prettyjson'],
    entry_points='''
        [console_scripts]
        pj=prettyjson.prettyjson:cli
        pjsettings=prettyjson.settings:cli
        pjdisplay=prettyjson.open:cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
