#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . dotmagic import DotMagics

def load_ipython_extension(ipython):
    """Load the extension in IPython."""
    ipython.register_magics(DotMagics)


def unload_ipython_extension(ipython):
    """Unload the extension in IPython."""
    pass

