from distutils.core import setup
import py2exe, sys, os

setup(
    options={'py2exe': {'bundle_files': '1', 'compressed': True}},
    console=['pathx.py'],
    zipfile=None
)
