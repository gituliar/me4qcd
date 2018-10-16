#!/usr/bin/env python3
"""qgraf.py - a user-friendly interface to QGRAF

Usage:
    qgraf.py [--form | --graph] [-v] [-x] [-o FILE] PROCESS

Arguments:
    -f, --form      Generate in FORM style.
    -g, --graph     Generate in GRAPH style [default]
    -x              Conjugate amplitude
    -v              Verbose mode
    -o FILE         Output file name [STDOUT by default].
    PROCESS         Amplitude to generate of <in>_<out>_<n> form, where
                      - <n>           loops count
                      - <in>, <out>   external legs
                          photon      a
                          quark       u, d
                          anti-quark  U, D
                          gluon       g
                    for example: a_uUg_1
"""


from   datetime import datetime
import os
import os.path
import shutil
import tempfile

import docopt

QGRAF_DAT = """
output= '%(output)s' ;
style= '%(style)s.sty' ;
model= 'qcd.mod' ;
in= %(in)s ;
out= %(out)s ;
loops= %(n)s ;
loop_momentum= l ;
options= ;
"""

QCD_MOD = """
#   PROPAGATORS
    [a, a, +, external;  prop_id='Pa']
    [u, U, -, notadpole; prop_id='Pu']
    [d, D, -, notadpole; prop_id='Pd']
    [g, g, +, notadpole; prop_id='Pg']

#   VERTICES
    [u, U, a;     vertex_id='Vqqa', vertex_factor='2/3']
    [d, D, a;     vertex_id='Vqqa', vertex_factor='-1/3']
    [u, U, g;     vertex_id='Vqqg', vertex_factor='1']
    [d, D, g;     vertex_id='Vqqg', vertex_factor='1']
    [g, g, g;     vertex_id='Vggg', vertex_factor='1']
    [g, g, g, g;  vertex_id='Vgggg', vertex_factor='1']
#
#     vertex_id is a name of a vertex function in FORM
"""

FORM_STY = """
<prologue>
*
* generated by <program> on {0:%Y-%m-%d}
*
<command_loop><command_line_loop>* <command_data><end><end>*
<diagram>
*--#[[ d<diagram_index>:
<minus><symmetry_factor>*
<in_loop>F<field>(<field_index>,<momentum>)*
<end><out_loop>F<field>(<field_index>,<momentum>)*
<end><propagator_loop>P<field>(<dual-field_index>,<field_index>,
<back><momentum>)*
<end><back>
<vertex_loop>[vertex_factor]*[vertex_id](<ray_loop><field_index>,<momentum>,
<back><end><back>)*
<end><back><back>
*--#]] d<diagram_index>:
<epilogue>
*--#[[ Declarations:
#$n = <diagram_index>;
*--#]] Declarations:
*
* end
*
<exit>
""".format(datetime.now())

GRAPH_STY = """
<prologue>
*
* generated by <program> on {0:%Y-%m-%d}
*
<command_loop><command_line_loop>* <command_data><end><end>*
<diagram>
#<diagram_index>
<in_loop><momentum> <vertex_index>
<end><back>
<out_loop><momentum> <vertex_index>
<end><back>
<propagator_loop><vertex_index> <dual-vertex_index> [prop_id]
<end><back>
<epilogue>
<exit>
""".format(datetime.now())

def mkfile(path, filename, data):
    with open(os.path.join(path, filename), 'w') as f:
        f.write(data)

def format_qgraf_dat(process, style, output):
    lst = args['PROCESS'].split('_')
    print(lst)
    # process may be '<in>2<out>_<n>' or '<in>_<out>_<n>'
    if len(lst) == 3:
        in_mask, out_mask, n = lst
    else:
        in_mask, out_mask = lst[0].split('2')
        n = lst[1]
    print(in_mask, out_mask)

    if len(in_mask) == 1:
        in_p = [in_mask[0]+'[q]']
    else:
        in_p =  [in_mask[0]+'[p1]', in_mask[1]+'[p2]']

    out_p = ["%s[k%d]" % (c, i) for c,i in zip(out_mask, range(1,len(out_mask)+1))]

    in_ = ', '.join(in_p)
    out = ', '.join(out_p)
    if args['-x']:
        in_, out = out, in_

    qgraf_dat = QGRAF_DAT % {
        'in': in_,
        'out': out,
        'n': n,
        'style': style,
        'output': output,
    }
    return qgraf_dat

if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    if args["-o"] is None:
        out_path, out_name = "", "STDOUT"
    else:
        out_path = args["-o"]
        out_name = os.path.basename(out_path)

    style = 'form' if args["--form"] is True else 'graph'

    qgraf_dat = format_qgraf_dat(args['PROCESS'], style, out_name)
    with tempfile.TemporaryDirectory() as td:
        mkfile(td, "qgraf.dat", qgraf_dat)
        mkfile(td, "qcd.mod", QCD_MOD)
        mkfile(td, "form.sty", FORM_STY)
        mkfile(td, "graph.sty", GRAPH_STY)

        cmd = "cd %s && qgraf" % (td,)
        if not args["-v"]:
            cmd += " > /dev/null"
        os.system(cmd)

        td_out_path = os.path.join(td, out_name)
        if not os.path.exists(td_out_path):
            raise docopt.DocoptExit(
                message="[ERROR] QGRAF failed to generate output file.\n        Use -v flag to see more details.\n")

        if args["-o"] is None:
            with open(td_out_path, 'r') as f:
                print(f.read())
        else:
            try:
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
            except FileNotFoundError:
                pass
            shutil.move(td_out_path, out_path)
