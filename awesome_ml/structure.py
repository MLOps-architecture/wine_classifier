"""Define global project (file-)structure here.

This module is used to define all filepaths and/or keys
used in the project. the __factory function is used to build
these paths or path templates on settings or environment variables.
"""
from drtools.core.filesystem import FileStructure

PATH = FileStructure(
    {
        'EVAL':         ('models', ),
        'DATA':         ('data', ),
        'RAW':              ('DATA', 'raw', ),
        'CS_IN':                ('RAW', 'clickstream.csv'),
        'PROCESSED':        ('DATA', 'processed', ),
        'CS_OUT':               ('PROCESSED', 'clickstream.pickle'),
    },
)
