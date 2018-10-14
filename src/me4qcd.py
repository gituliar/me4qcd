#!/usr/bin/env python3
"""me4qcd.py - makes squared matrix elements

Usage:
    me4qcd.py AMP1 AMP2 ME2

Arguments:
    AMP1 AMP2       Amplitude files to use (outpur of `qgraf.py --form')
    ME2
"""

import os
import subprocess
import tempfile

import docopt

ROOT_PATH = os.path.normpath(os.path.realpath(__file__)+'/../..')

def split_amp(name):
    pass

if __name__ == "__main__":
    args = docopt.docopt(__doc__)

    with tempfile.TemporaryDirectory() as td:
        cmd = [
          'tform',
          '-w2',
          '-t', td,
          '-ts', td,
          '-I', os.path.join(ROOT_PATH,'src'),
          '-d', 'AMP='+args['AMP1'],
          '-d', 'AMPx='+args['AMP2'],
          '-d', 'ME2='+args['ME2'],
          os.path.join(ROOT_PATH,'src/me4qcd.frm')]
        try:
            subprocess.call(cmd, shell=False)
        except Exception as error:
            #print(error)
            pass
