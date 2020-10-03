#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import string
import tempfile
from pkg_resources import resource_filename
from IPython.display import SVG, Image
from IPython.core.magic import (
    Magics, magics_class,
    line_magic, line_cell_magic
)


class Cmd:

    def __init__(self, cmd, stdin=PIPE, stdout=PIPE, stderr=None, outfile=None):
        self._proc = Popen(cmd, stdin=stdin, stdout=stdout, stderr=stderr)
        self._outfile = outfile

    def send(self, data):
        self._proc.stdin.write(data)

    def close(self):
        self._proc.stdin.close()

    def read(self):
        self._proc.wait()
        if self._outfile:
            with open(self._outfile, 'rb') as fh:
                return fh.read()
        return self._proc.stdout.read()

    def pipe(self, cmd, outfile=None):
        return Cmd(cmd, self._proc.stdout, outfile=outfile)

    def __or__(self, other):
        return self.pipe(other)


@magics_class
class DotMagics(Magics):


    def __init__(self, shell=None, **kwargs):
        super().__init__(shell, **kwargs)
        self._opts = 'prsK:'
        self._tmpdir = tempfile.mkdtemp()


    def _run_graphviz(self, s, output='svg', layout='dot'):
        cmd = ['dot', '-T', output, '-K', layout]
        c = Cmd(cmd)
        c.send(s.encode())
        c.close()
        return c

    def _drop_shadow(self, source):
        xsl_file = resource_filename(__name__, 'notugly.xsl')
        cmd = ['xsltproc', '--nonet', xsl_file, '-']
        return source.pipe(cmd)

    def _svg_to_png(self, s):
        _, tmpf = tempfile.mkstemp(dir=self._tmpdir, suffix='.png')
        cmd = ['inkscape', '-p', '-o', tmpf]
        return s.pipe(cmd, outfile=tmpf)

    def _do_args(self, line):
        return self.parse_options(line, self._opts)
        
    def _do_magic(self, opts, line, cell=None):
        layout = opts.get('K', 'dot')

        s = line
        
        if cell:
            s = '\n' + cell

        image_type = SVG

        s = string.Template(s)
        s = s.safe_substitute(self.shell.user_ns)

        cmd = self._run_graphviz(s, layout=layout)

        if 's' in opts:
            cmd = self._drop_shadow(cmd)

        if 'p' in opts:
            cmd = self._svg_to_png(cmd)
            image_type = Image

        if 'r' in opts:
            return cmd.read()

        out = cmd.read()
        return image_type(out)


    @line_cell_magic
    def dot(self, line, cell=None):
        opts, line = self._do_args(line)
        return self._do_magic(opts, line, cell)

    @line_magic
    def dotstr(self, line):
        opts, line = self._do_args(line)
        line = self.shell.ev(line)
        return self._do_magic(opts, line)
