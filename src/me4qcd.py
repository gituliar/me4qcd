#!/usr/bin/env python3
"""me4qcd.py - makes squared matrix elements

Usage:
    me4qcd.py init AMP AMPX OUTDIR
    me4qcd.py sort [-d] INDIR OUTDIR
    me4qcd.py col INDIR OUTDIR
    me4qcd.py num INDIR OUTDIR
    me4qcd.py collect INDIR OUTFILE
    me4qcd.py frm2math INFILE OUTFILE

Arguments:
    AMP AMPX       Amplitude files to use (outpur of `qgraf.py --form')
    INDIR
    OUTDIR
"""

import logging
import os
import subprocess
import tempfile

import docopt


def main(args):
    logging.debug("Command-line arguments:\n%s", args)
    for name in ['init','sort','col','num','collect','frm2math']:
        if not args[name]:
            continue
        cmd = globals().get('cmd_'+name)
        cmd(args)
        break

# ------------------------------------------------------------------------------------------------ #
#                                        Command Handlers                                          #
# ------------------------------------------------------------------------------------------------ #
def cmd_init(args):
    n1, n2 = amp_count(args['AMP']), amp_count(args['AMPX'])
    mkdir(args['OUTDIR'])
    for i in range(1,n1+1):
        for j in range(1, n2+1):
            outfile = os.path.join(args['OUTDIR'], "%d_%d.h" % (i,j))
            if valid_output(outfile):
                continue
            touch(outfile)
            logging.info("make '%s'" % outfile)
            form(
              ME2RAW_FRM, 'me2raw', [
              '-d', 'AMP='+args['AMP'],
              '-d', 'AMPX='+args['AMPX'],
              '-d', 'OUTFILE='+outfile,
              '-d', 'i='+str(i),
              '-d', 'j='+str(j),
            ])


def cmd_frm2math(args):
    form(
        FRM2MATH_FRM, 'frm2math', [
        '-d','INFILE='+args['INFILE'],
        '-d','OUTFILE='+args['OUTFILE'],
    ])


def cmd_sort(args):
    indir, outdir = args['INDIR'], args['OUTDIR']
    mkdir(outdir)
    for name in os.listdir(indir):
        infile = os.path.join(indir, name)
        sort(infile, outdir)
        #if args['-d']:
        #    os.remove(infile)


def sort(infile, outdir):
    col_outfile = os.path.join(outdir, os.path.basename(infile[:-2])) + ".col.h"
    if os.path.exists(col_outfile):
        logging.debug("'%s' already sorted" % infile)
        return
    with open(infile) as f:
        buf = f.read().replace('\n','').replace(' ','')
        amps = sort_helper(buf)
    if amps is None:
        logging.warning("'%s' is empty" % infile)
        return
    #if len(amps) == 1 and len(amps[0]) == 1:
    #    logging.info("'%s' already sorted" % infile)
    #    return
    for amp in amps:
        outname = os.path.join(outdir, os.path.basename(infile[:-2]))
        if 'idx' in amp:
            outname += '_'+amp['idx'][0][1:-1]
        for suf, funs in {'num':('gm','num'),'den':('den',),'col':('col',)}.items():
            if not any(map(lambda fun: fun in amp, funs)):
                continue
            i = 0
            outfile = outname+'.'+suf+'.h'
            if os.path.exists(outfile):
                logging.debug("'%s' already exists" % outfile)
                continue
            with open(outfile, 'w') as f:
                for fun, fun_args in amp.items():
                    if fun not in funs:
                        continue
                    logging.info("make '%s'" % outfile)
                    for arg in fun_args:
                        if i > 0:
                            f.write('*\n')
                        i = 1
                        f.write(fun)
                        f.write(arg)

def sort_helper(buf):
    k = 0
    amps, amp = [], {}
    while k < len(buf):
        i,j = k,k
        # parse function name
        while buf[k].isalpha():
            k += 1
        fun = buf[i:k]
        # parse function arguments
        j = k
        d = 1
        k += 1
        while d > 0:
            if buf[k] == '(':
                d += 1
            elif buf[k] == ')':
                d -= 1
            k += 1
        if k < len(buf) and buf[k] == '^':
            k += 1
            while k < len(buf) and buf[k].isdigit():
                k += 1
        arg = buf[j:k]
        # append parsed function to the current amplitude
        if fun not in amp:
            amp[fun] = [arg]
        else:
            amp[fun].append(arg)

        # exit?
        if k >= len(buf):
            amps.append(amp)
            return amps
        # next amplitude?
        elif buf[k] == '+':
            amps.append(amp)
            amp = {}
        # read next function
        k += 1
    amps



def cmd_col(args):
    indir, outdir = args['INDIR'], args['OUTDIR']
    mkdir(outdir)
    for name in os.listdir(indir):
        infile, outfile = os.path.join(indir, name), os.path.join(outdir, name)
        if invalid_input(infile, '.col.h') or valid_output(outfile, infile):
            continue
        touch(outfile)
        logging.info("make '%s'" % outfile)
        form(
            COL_FRM, 'col', [
            '-d','INFILE='+infile,
            '-d','OUTFILE='+outfile,
        ])


def cmd_num(args):
    indir, outdir = args['INDIR'], args['OUTDIR']
    mkdir(outdir)
    for name in os.listdir(indir):
        infile, outfile = os.path.join(indir, name), os.path.join(outdir, name)
        if invalid_input(infile, '.num.h') or valid_output(outfile, infile):
            continue
        touch(outfile)
        logging.info("make '%s'" % outfile)
        form(
            NUM_FRM, 'num', [
            '-d','INFILE='+infile,
            '-d','OUTFILE='+outfile,
        ])


def cmd_collect(args):
    indir, outfile = args['INDIR'], args['OUTFILE']
    names = [name[:-6] for name in os.listdir(indir) if name.endswith('.num.h')]
    with open(args['OUTFILE'], 'w') as fout:
        fout.write('0')
        for name in names:
            infile = os.path.join(indir, name)
            fout.write('+1')
            fout.write('*amp(%s)' % name.replace('_',','))
            for tag in ['col','den','num']:
                filename = os.path.join(indir, name+'.'+tag+'.h')
                if os.path.exists(filename):
                    with open(filename, 'r') as fin:
                        ex = fin.read()
                    fout.write('*(')
                    fout.write(ex)
                    fout.write(')')

# ------------------------------------------------------------------------------------------------ #
#                                             Helpers                                              #
# ------------------------------------------------------------------------------------------------ #
def amp_count(filename):
    with open(filename, 'r') as amp:
        for line in amp:
            if line.startswith('#$n ='):
                return int(line[6:-2])

def form(src, name, args):
    if not hasattr(form, 'src'):
        form.src = {}
    if name not in form.src:
        f = tempfile.NamedTemporaryFile(mode='w', prefix=name+'.', suffix='.frm', delete=False)
        f.write(src)
        f.close()
        form.src[name] = f.name
    f_name = form.src[name]
    command = ['form', '-q'] + args + [f_name]
    logging.debug("call \"%s\"" % " ".join(command))
    try:
        subprocess.call(command, shell=False)
    except Exception as error:
       logging.error(error)

def invalid_input(infile, suffix=""):
     return not(os.path.isfile(infile) and infile.endswith(suffix))

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logging.info("create '%s'" % path)

def touch(name):
    #logging.debug("touch '%s'" % name)
    open(name,'w').close()

def valid_output(outfile, infile=None):
    # TODO compare infile and outfile modification dates
    if os.path.isfile(outfile):
        logging.debug("file exists '%s'" % outfile)
        return True
    return False




FRM2MATH_FRM = """
Off Statistics;
#define RANK "12"

Vector cOlpR1,...,cOlpR`RANK',cOlpA1,...,cOlpA`RANK';
CFunction d33,d44,d55,d433,d66,d633,d543,d444,d3333
	,d77,d743,d653,d644,d554,d5333,d4433a,d4433b,d4433c
	,d88,d853,d844,d763,d754,d7333,d664,d655,d6433a,d6433b,d6433c
	,d5533a,d5533b,d5533c,d5533d,d5443a,d5443b,d5443c,d5443d
	,d4444a,d4444b,d43333a,d43333b;

CF amp, col, den, num, sp;
S  m, NF,NA,,Ca,Cf,Na,Tf,nf;

* momenta
V k1,...,k9;
V l1,...,l9;
V p1,p2;
V q;

* helpers
S ex1,ex2,ex3;

.sort

L F =
  (
  #include `INFILE'
  );
.sort

id p1?.p2? = sp(p1,p2);

Bracket amp,col,den;
.sort
Collect num;

Format Mathematica;
#write <`OUTFILE'> "(%E)", F
.end
"""



NUM_FRM = """
Off Statistics;

CF gm, num, e,i;
S  m, ex1;
Dimension m;

* momenta
V k1,...,k9;
V l1,...,l9;
V p1,p2;
V q;

* helpers
S ex1,ex2,ex3;

#define N "200";
#do i=1,`N'
I mu`i'=m;
I mui`i'=m;
I mue`i'=m;
#enddo

.sort

L F =
  (
  #include `INFILE'
  );
.sort


repeat id gm(ex1?,ex2?,?arg1)*gm(ex2?,ex3?,?arg2) = gm(ex1,ex3,?arg1,?arg2);

#do i={1,2,3,4,5}
id once gm(ex1?,ex1?,?arg1) = gm(`i',?arg1);
repeat;
  id gm(`i',k1?,?arg)  = g_(`i',k1)*gm(`i',?arg);
  id gm(`i',mu1?,?arg) = g_(`i',mu1)*gm(`i',?arg);
  id gm(`i') = 1;
endrepeat;
tracen `i';
#enddo

id q.q = 1;
id p1.p2 = 1/2;
id p1.p1 = 0;
id p2.p2 = 0;
#do i=1,9
id k`i'.k`i' = 0;
#enddo
.sort


id num(ex1?) = ex1;

id q.q = 1;
id p1.p2 = 1/2;
id p1.p1 = 0;
id p2.p2 = 0;
#do i=1,9
id k`i'.k`i' = 0;
#enddo
.sort

#write <`OUTFILE'> "%E", F
.end
"""




ME2RAW_FRM = """
Off Statistics;

CF amp,ampx, col, den, num, gm, sp, idx;
S  m,ep, NF,NA,  Ca,Cf,Na,Tf,nf;
Tensor T, f(antisymmetric);

#define N "200";
#do k=1,`N'
I cj`k'=NA;
I cii`k'=NF;
I cie`k'=NF;
I cji`k'=NA;
I cje`k'=NA;
I mu`k'=m;
I mui`k'=m;
I mue`k'=m;
#enddo
Set cii:cii1,...,cii`N';
Set cie:cie1,...,cie`N';
Set cji:cji1,...,cji`N';
Set cje:cje1,...,cje`N';
Set mui:mui1,...,mui`N';
Set mue:mue1,...,mue`N';

* Feynman rules
CF Vqqg,Vqqa,Vggg,Vgggg;
CF vggg,vgggg;
CF Pu, Pd, Pg, Pax, Pux,PUx, Pdx,PDx, Pgx;
CF Fa, Fu,FU, Fd,FD, Fg;
CF e,i;

* Momenta
V k1,...,k9;
V l1,...,l9;
V p1,p2;
V q;

* Helpers
S ex1,ex2,ex3;
S n1,...,n4;

* ------------------------------------------------------------------------------
*                              1. Read Amplitudes
* ------------------------------------------------------------------------------

* Here, AMP and AMPX are generated with `drqgraf' with the same <in>_<out>, but one
* with '-x' option used. (That is with <in> and <out> exchanged, e.g., AMPX.in = AMP.out).

* ------------------------------------------------------------------------------
*                                1.1 Read AMPX
* ------------------------------------------------------------------------------
#include `AMPX' # Declarations
L AMPX =
  (
  #include `AMPX' # d`j'
  );
;
* Since AMP and AMPX are generated by QGRAF independently their indices overlap.
* That makes impossible to restore a propper order of propagators when
* both are combined into ME2. We fix this by bumping indices in AMPX.
#define DI "100"
#do F={Fa, Fu, FU, Fd, FD, Fg} 
id `F'(n1?neg_,k1?) = `F'(n1-`DI',k1);
#enddo
#do P={Pu, Pd, Pg} 
id `P'(n1?pos_, n2?,k1?) = `P'(n1+`DI',n2,k1);
id `P'(n1?, n2?pos_,k1?) = `P'(n1,n2+`DI',k1);
#enddo
#do V={Vqqa, Vqqg, Vggg} 
id `V'(n1?pos_,k1?, n2?,k2?, n3?,k3?) = `V'(n1+`DI',k1, n2,k2, n3,k3);
id `V'(n1?,k1?, n2?pos_,k2?, n3?,k3?) = `V'(n1,k1, n2+`DI',k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, n3?pos_,k3?) = `V'(n1,k1, n2,k2, n3+`DI',k3);
id `V'(n1?neg_,k1?, n2?,k2?, n3?,k3?) = `V'(n1-`DI',k1, n2,k2, n3,k3);
id `V'(n1?,k1?, n2?neg_,k2?, n3?,k3?) = `V'(n1,k1, n2-`DI',k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, n3?neg_,k3?) = `V'(n1,k1, n2,k2, n3-`DI',k3);
#enddo
id Vgggg(n1?pos_,k1?, n2?,k2?, n3?,k3?, n4?,k4?) = Vgggg(n1+`DI',k1, n2,k2, n3,k3, n4,k4);
id Vgggg(n1?,k1?, n2?pos_,k2?, n3?,k3?, n4?,k4?) = Vgggg(n1,k1, n2+`DI',k2, n3,k3, n4,k4);
id Vgggg(n1?,k1?, n2?,k2?, n3?pos_,k3?, n4?,k4?) = Vgggg(n1,k1, n2,k2, n3+`DI',k3, n4,k4);
id Vgggg(n1?,k1?, n2?,k2?, n3?,k3?, n4?pos_,k4?) = Vgggg(n1,k1, n2,k2, n3,k3, n4+`DI',k4);
id Vgggg(n1?neg_,k1?, n2?,k2?, n3?,k3?, n4?,k4?) = Vgggg(n1-`DI',k1, n2,k2, n3,k3, n4,k4);
id Vgggg(n1?,k1?, n2?neg_,k2?, n3?,k3?, n4?,k4?) = Vgggg(n1,k1, n2-`DI',k2, n3,k3, n4,k4);
id Vgggg(n1?,k1?, n2?,k2?, n3?neg_,k3?, n4?,k4?) = Vgggg(n1,k1, n2,k2, n3-`DI',k3, n4,k4);
id Vgggg(n1?,k1?, n2?,k2?, n3?,k3?, n4?neg_,k4?) = Vgggg(n1,k1, n2,k2, n3,k3, n4-`DI',k4);

* ------------------------------------------------------------------------------
*                            1.1.1 Complex Conjugate
* ------------------------------------------------------------------------------
* These propagators and vertices change sign when complex conjugates.
* We also include Vggg since f_abc is antysymmetric.
#do X={Pg,Pu,Pd, Vqqg,Vqqa,Vgggg,Vggg} 
id `X'(?args) = -`X'(?args);
#enddo
$n2 = $n;
.sort

* ------------------------------------------------------------------------------
*                                1.2 Read AMP
* ------------------------------------------------------------------------------
#include `AMP' # Declarations
L AMP =
  (
  #include `AMP' # d`i'
  );
$n1 = $n;
.sort

* ------------------------------------------------------------------------------
*                                 2. Build ME2
* ------------------------------------------------------------------------------
L ME2 = AMP*AMPX;
.sort
Drop AMP,AMPX;


* Connect external lines (polarization sum)
#do x={a,g,u,d} 
id F`x'(n1?even_,k1?)*F`x'(n2?odd_,k1?) = P`x'x(n1,n2,k1);
#enddo
id FU(n1?even_,k1?)*FU(n2?odd_,k1?) = Pux(n2,n1,k1);
id FD(n1?even_,k1?)*FD(n2?odd_,k1?) = Pdx(n2,n1,k1);

* Make all indices positive
#do P={Pu, Pd, Pg} 
id `P'(n1?,n2?,k1?) = `P'(i(n1),i(n2),k1);
#enddo
#do P={Pax, Pux, Pdx, Pgx} 
id `P'(n1?,n2?,k1?) = `P'(e(-n1),e(-n2),k1);
#enddo

#do V={Vqqa, Vqqg, Vggg} 
id `V'(n1?pos_,k1?, n2?,k2?, n3?,k3?) = `V'(i(n1),k1, n2,k2, n3,k3);
id `V'(n1?,k1?, n2?pos_,k2?, n3?,k3?) = `V'(n1,k1, i(n2),k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, n3?pos_,k3?) = `V'(n1,k1, n2,k2, i(n3),k3);
id `V'(n1?neg_,k1?, n2?,k2?, n3?,k3?) = `V'(e(-n1),k1, n2,k2, n3,k3);
id `V'(n1?,k1?, n2?neg_,k2?, n3?,k3?) = `V'(n1,k1, e(-n2),k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, n3?neg_,k3?) = `V'(n1,k1, n2,k2, e(-n3),k3);
#enddo
id Vgggg(n1?neg_,k1?, n2?,k2?, n3?,k3?, n4?,k4?) = Vgggg(e(-n1),k1, n2,k2, n3,k3, n4,k4);
id Vgggg(n1?,k1?, n2?neg_,k2?, n3?,k3?, n4?,k4?) = Vgggg(n1,k1, e(-n2),k2, n3,k3, n4,k4);
id Vgggg(n1?,k1?, n2?,k2?, n3?neg_,k3?, n4?,k4?) = Vgggg(n1,k1, n2,k2, e(-n3),k3, n4,k4);
id Vgggg(n1?,k1?, n2?,k2?, n3?,k3?, n4?neg_,k4?) = Vgggg(n1,k1, n2,k2, n3,k3, e(-n4),k4);
id Vgggg(n1?pos_,k1?, n2?,k2?, n3?,k3?, n4?,k4?) = Vgggg(i(n1),k1, n2,k2, n3,k3, n4,k4);
id Vgggg(n1?,k1?, n2?pos_,k2?, n3?,k3?, n4?,k4?) = Vgggg(n1,k1, i(n2),k2, n3,k3, n4,k4);
id Vgggg(n1?,k1?, n2?,k2?, n3?pos_,k3?, n4?,k4?) = Vgggg(n1,k1, n2,k2, i(n3),k3, n4,k4);
id Vgggg(n1?,k1?, n2?,k2?, n3?,k3?, n4?pos_,k4?) = Vgggg(n1,k1, n2,k2, n3,k3, i(n4),k4);
.sort


* ------------------------------------------------------------------------------
*                               2.1 Feynman Rules
* ------------------------------------------------------------------------------
*  References:
*    - Itzykson, Zuber (pp. 801-802)
*    - Peskin, Schroeder (pp. 698-700)
*
* ------------------------------------------------------------------------------
*
*                                Polarization Sum
*                               ~~~~~~~~~~~~~~~~~~
id Pax(e(n1?), e(n2?), k1?) = -d_(mue[n1],mue[n2]);
id Pgx(e(n1?), e(n2?), k1?) = col(-d_(cje[n1],cje[n2])) * d_(mue[n1],mue[n2]);
#do Px={Pux,Pdx} 
id `Px'(e(n1?), e(n2?), k1?) = col(d_(cie[n1],cie[n2]))* gm(e(n2),e(n1),k1);
#enddo
*
*                                   Propagatos
*                                  ~~~~~~~~~~~~
#do P={Pu,Pd} 
id `P'(i(n1?), i(n2?), k1?) = col(i_*d_(cii[n1],cii[n2])) * gm(i(n2),i(n1),k1) * den(sp(k1));
#enddo
id Pg(i(n1?), i(n2?), k1?) = col(-i_*d_(cji[n1],cji[n2])) * d_(mui[n1],mui[n2]) * den(sp(k1));
.sort
*
*                                    Vertices
*                                   ~~~~~~~~~~
#do a={e,i} 
#do b={e,i} 
#do c={e,i} 
  id Vqqa(`a'(n1?),k1?, `b'(n2?),k2?, `c'(n3?),k3?) =
      col(i_*d_(ci`a'[n1],ci`b'[n2])) *
        gm(`b'(n2),`a'(n1),mu`c'[n3]);
  id Vqqg(`a'(n1?),k1?, `b'(n2?),k2?, `c'(n3?),k3?) =
      col(i_*T(ci`a'[n1],ci`b'[n2],cj`c'[n3])) *
        gm(`b'(n2),`a'(n1),mu`c'[n3]);
  id Vggg(`a'(n1?),k1?, `b'(n2?),k2?, `c'(n3?),k3?) =
      col(f(cj`a'[n1],cj`b'[n2],cj`c'[n3])) *
        vggg(mu`a'[n1],k1, mu`b'[n2],k2, mu`c'[n3],k3);
  #do d={e,i} 
  #do i=1,10
  id once Vgggg(`a'(n1?),k1?, `b'(n2?),k2?, `c'(n3?),k3?, `d'(n4?),k4?) =
      col(-i_*f(cj`a'[n1],cj`b'[n2],cj`i')*f(cj`c'[n3],cj`d'[n4],cj`i')) *
        idx(4^(`i'-1)*1) *
        vgggg(mu`a'[n1], mu`b'[n2], mu`c'[n3], mu`d'[n4]) +
      col(-i_*f(cj`a'[n1],cj`c'[n3],cj`i')*f(cj`b'[n2],cj`d'[n4],cj`i')) * 
        idx(4^(`i'-1)*2) *
        vgggg(mu`a'[n1], mu`c'[n3], mu`b'[n2], mu`d'[n4]) +
      col(-i_*f(cj`a'[n1],cj`d'[n4],cj`i')*f(cj`b'[n2],cj`c'[n3],cj`i')) *
        idx(4^(`i'-1)*3) *
        vgggg(mu`a'[n1], mu`d'[n4], mu`b'[n2], mu`c'[n3]) ;
  #enddo
#enddo
#enddo
#enddo
#enddo
repeat id idx(ex1?)*idx(ex2?) = idx(ex1+ex2);
.sort

id vggg(mu1?,k1?, mu2?,k2?, mu3?,k3?) =
   num(d_(mu1,mu2)*(-k2(mu3)+k1(mu3)) +
       d_(mu2,mu3)*(-k3(mu1)+k2(mu1)) +
       d_(mu3,mu1)*(-k1(mu2)+k3(mu2)));
id vgggg(mu1?, mu2?, mu3?, mu4?) =
   num(d_(mu1,mu3)*d_(mu2,mu4) - d_(mu1,mu4)*d_(mu2,mu3));


Bracket den,gm,num,col,idx;
.sort

* Pull overall factor into col(..)
Collect col;
repeat id col(ex1?)*col(ex2?) = col(ex1*ex2);
.sort

#write <`OUTFILE'> "%E", ME2
#close <`OUTFILE'>
.end
"""


COL_FRM = """
Off Statistics;

* #include color.h
%s

CF col;
S  m, NF,NA,  Ca,Cf,Na,Tf,nf;
S  ex1;

#define N "200";
#do i=1,`N'
I cj`i'=NA;
I cii`i'=NF;
I cie`i'=NF;
I cji`i'=NA;
I cje`i'=NA;
I mu`i'=m;
I mui`i'=m;
I mue`i'=m;
#enddo

.sort

L F =
  (
  #include `INFILE'
  );
.sort

id col(ex1?) = ex1;
.sort

#call docolor;

id cA = Ca;
id cR = Cf;
id I2R = Tf;
id NA = Na;
id 1/NA = 1/Na;
*id Tf = Tf*nf;
.sort

#write <`OUTFILE'> "col(%%E)", F
.end
""" % """
#define RANK "6"
*
*	The file with all the declarations for running color traces.
*	The variable RANK tells how many Adjoint invariants of how many
*	non-adjoint invariants can occur simultaneously. For 14 vertices
*	this number is maximally 4 (4 loops in a non-adjoint representation)
*
*	Note: One needs version 3 of FORM to run this.
*	Version 2 (or 2.3) makes no chance. The program would need very
*	extensive reworking and it would become far less efficient.
*	All internal variables start with the string cOl to avoid potential 
*	conflicts with namings in the calling program.
*
*	The external variables are:
*	Tensor T;
*	Tensor f(antisymmetric);
*	Symbol NA;
*	Symbol NR;
*	Symbol I2R;
*	Symbol cA;
*	Symbol cR;
*	Symbol [cR-cA/2];
*	All generic d contractions like d33, d763 etc. which are CFunctions.
*
*	File by J.Vermaseren, 24-may-1997
*
*--#[ Declarations :
*
Symbol NA,NR,I2R;
Dimension NA;
AutoDeclare Index cOli,cOlj,cOlk,cOln;
AutoDeclare Symbol cOlI;
AutoDeclare Vector cOlp,cOlq;
AutoDeclare Symbol cOlx,cOly,cOlc;
AutoDeclare Tensor cOld;
AutoDeclare Tensor cOldr(symmetric),cOlda(symmetric);
Vector cOlpR1,...,cOlpR`RANK',cOlpA1,...,cOlpA`RANK';
Tensor cOldR1,...,cOldR`RANK',cOldA1,...,cOldA`RANK';
Tensor,<cOldr1(symmetric)>,...,<cOldr`RANK'(symmetric)>
		,<cOlda1(symmetric)>,...,<cOlda`RANK'(symmetric)>;
Symbol cOln, cA,cR,[cR-cA/2];
Tensor cOlfp,cOlff(cyclic),T,cOlTr(cyclic),cOlTt(cyclic),cOlf3;
NTensor cOlTN,cOlTM;
CFunction cOlTT,cOlnum,cOldddff,cOldff554,cOld,cOldd,cOlddd,cOlorig,cOlacc;
CFunction cOlE,cOlE0,cOlEa,cOlEb,cOlEc,cOldexp;
CFunction d33,d44,d55,d433,d66,d633,d543,d444,d3333
	,d77,d743,d653,d644,d554,d5333,d4433a,d4433b,d4433c
	,d88,d853,d844,d763,d754,d7333,d664,d655,d6433a,d6433b,d6433c
	,d5533a,d5533b,d5533c,d5533d,d5443a,d5443b,d5443c,d5443d
	,d4444a,d4444b,d43333a,d43333b;
Tensor f(antisymmetric),cOlf1(antisymmetric);
Set cOlpAs:cOlpA1,...,cOlpA`RANK';
Set cOlpRs:cOlpR1,...,cOlpR`RANK';
Set cOlpAR:cOlpA1,...,cOlpA`RANK',cOlpR1,...,cOlpR`RANK';
Set cOldar:cOlda1,...,cOlda`RANK',cOldr1,...,cOldr`RANK';
Set cOldas:cOlda1,...,cOlda`RANK';
Set cOliii:cOli1,...,cOli30;
Set cOljjj:cOlj1,...,cOlj30;
ProperCount ON;
*
*--#] Declarations : 
*--#[ SORT :
*
*	Next Procedure handles the .sort. This way one can put the program
*	in a checking mode in which there is printing at all .sort instructions
*	by just adding a single statement.
*
#procedure SORT(text)
*Print +f +s;
.sort:`text';
#endprocedure
*
*--#] SORT : 
*--#[ color :
*
#procedure color
*
*	Main routine for color traces.
*	We need the declarations of the file cfactors.h in the main program.
*	The algorithm is following the paper.
*	We have included some extra reductions for
*	cOlTr( cOli1,cOli2,cOli3,cOli4,...,cOli1,cOli2,cOli3,cOli4,...) and cOlTr( cOli1,cOli2,cOli3,...,cOli1,cOli2,cOli3,...)
*	because that helps very much in some cases.
*
*	If the variable ALTERNATEMETHOD is defined we follow a different
*	order of elimination. This can be useful for deriving identities that
*	are otherwise far from trivial.
*
*	Routine by J.Vermaseren, 24-may-1997
*
#define ik1 "0"
repeat id T(cOli1?,cOli2?,?a)*T(cOli2?,cOli3?,?b) = T(cOli1,cOli3,?a,?b);
id  T(cOli1?,cOli1?,?a) = cOlTr(?a);
*
* We work only with the TR. If there are leftover T we don't
* do anything.
*
if ( count(cOlTr,1) > 0 ) redefine ik1 "1";
#call SORT(color-1)
#ifndef `ALTERNATEMETHOD'
#call adjoint
#endif
#if `ik1' != 0
#do ik1a = 1,1
*
* First try to contract indices. The easy contractions first.
*
repeat;
  id  cOlTr(cOli1?,cOli1?,?a) = cR*cOlTr(?a);
  id  cOlTr(cOli1?,cOli2?,cOli1?,?a) = [cR-cA/2]*cOlTr(cOli2,?a);
  id  cOlTr(cOli1?,cOli2?,?a)*f(cOli1?,cOli2?,cOli3?) = i_*cA/2*cOlTr(cOli3,?a);
  if ( match(cOlTr(cOli1?,cOli2?,cOli3?,cOli4?,?b,cOli1?,cOli2?,cOli3?,cOli4?,?a)) );
    repeat;
      id  cOlTr(cOli1?,cOli2?,cOli3?,cOli4?,?b,cOli1?,cOli2?,cOli3?,cOli4?,?a) =
         + cOlTr(cOli1,cOli2,cOli3,cOli4,?b,cOli4,cOli3,cOli2,cOli1,?a)
         - 3*cOlTr(cOli1,cOli2,cOli3,?b,cOli3,cOli2,cOli1,?a)*cA
         + 7/4*cOlTr(cOli1,cOli2,?b,cOli2,cOli1,?a)*cA^2
         - 1/12*cOlTr(cOli1,?b,cOli1,?a)*cA^3
         + cOlTr(cOli1,cOli2,?b,cOli3,cOli4,?a)*cOldA(cOli1,cOli2,cOli3,cOli4)
         + 2*cOlTr(cOli1,cOli2,cOli3,?b,cOli3,cOli4,cOlk1,?a)*f(cOli1,cOlk1,cOlk2)*f(cOli2,cOli4,cOlk2)
         + 2*cOlTr(cOli1,cOli2,cOli3,?b,cOli4,cOlk1,cOli1,?a)*f(cOli2,cOlk1,cOlk2)*f(cOli3,cOli4,cOlk2)
         - cOlTr(cOli1,cOli2,cOli3,?b,cOli4,cOlk1,?a)*f(cOli1,cOlk1,cOlk2)*f(cOli2,cOlk2,cOlk3)*f(cOli3,cOli4,cOlk3)*i_
         + cOlTr(cOli1,cOli2,?b,cOli3,cOli4,cOlk1,?a)*f(cOli1,cOlk1,cOlk2)*f(cOli2,cOli3,cOlk3)*f(cOli4,cOlk2,cOlk3)*i_
         - 11/6*cOlTr(cOli1,cOli2,?b,cOli3,cOli4,?a)*f(cOli1,cOli4,cOlk1)*f(cOli2,cOli3,cOlk1)*cA;
      sum cOlk1,cOlk2,cOlk3;
      if ( count(cOldA,1) > 0 );
        #do isbb = 1,`RANK'
          if ( count(cOlpA`isbb',1) == 0 );
              id,once,cOldA(?a) = cOldA`isbb'(?a);
              ToVector,cOldA`isbb',cOlpA`isbb';
          endif;
        #enddo
      endif;
    endrepeat;
  endif;
  if ( match(cOlTr(cOli1?,cOli2?,cOli3?,?b,cOli1?,cOli2?,cOli3?,?a)) );
    repeat;
      id  cOlTr(cOli1?,cOli2?,cOli3?,?b,cOli1?,cOli2?,cOli3?,?a) =
           + 1/4*cOlTr(cOli1,?b,cOli1,?a)*cA^2
           - 3/2*cOlTr(cOli1,cOli2,?b,cOli2,cOli1,?a)*cA
           + cOlTr(cOli1,cOli2,?b,cOli3,cOlk4,?a)*f(cOli1,cOlk4,cOlk5)*f(cOli2,cOli3,cOlk5)
           + cOlTr(cOli1,cOli2,cOli3,?b,cOli3,cOli2,cOli1,?a);
      sum cOlk4,cOlk5;
    endrepeat;
  endif;
  id  cOlTr(cOli1?,cOli2?,?b,cOli1?,cOli2?,?a) = cOlTr(cOli1,cOli2,?b,cOli2,cOli1,?a)
            -cA/2*cOlTr(cOli1,?b,cOli1,?a);
  ReplaceLoop,f,a=3,l<4,outfun=cOlff;
  id  cOlff(cOli1?,cOli2?) = -cA*d_(cOli1,cOli2);
  id  cOlff(cOli1?,cOli2?,cOli3?) = cA/2*f(cOli1,cOli2,cOli3);
endrepeat;
id  cOlTr = I2R*NA/cR;
*
* Take the trace with the lowest number of different indices
*
id  cOlTr(?a) = cOlTT(?a,cOlTr(?a));
repeat id cOlTT(?a,cOli1?,?b,cOli1?,?c) = cOlTT(?a,?b,?c);
id  cOlTT(?a,cOlx?) = cOlTT(nargs_(?a),cOlx);
repeat;
  id,once,cOlTT(cOlx1?,cOly1?)*cOlTT(cOlx2?,cOly2?) =
    cOlTT(cOlx1,cOly1)*cOly2*theta_(cOlx2-cOlx1)+cOlTT(cOlx2,cOly2)*cOly1*theta_(cOlx1-cOlx2-1);
endrepeat;
id  cOlTT(cOlx?,cOlTr(?a)) = cOlTt(?a);
if ( count(cOlTr,1) > 0 ) redefine ik1a "0";
AB	cR,cA,[cR-cA/2];
#call SORT(color-2)
Keep brackets;
#do ik1c = 1,1
repeat;
  repeat;
    repeat;
      repeat;
        id  cOlTt(cOli1?,cOli1?,?a)   = cR*cOlTt(?a);
        id  cOlTt(cOli1?,cOli2?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,?a);
        id  cOlTt(cOli1?,cOli2?,?a)*f(cOli1?,cOli2?,cOli3?) = i_*cA/2*cOlTt(cOli3,?a);
      endrepeat;
      id cOlTt = I2R*NA/cR;
      if ( match(cOlTt(cOli1?,cOli2?,cOli3?,?b,cOli1?,cOli2?,cOli3?,?a)) );
        id  cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,?b,cOli1?,cOli2?,cOli3?,cOli4?,?a) =
           + cOlTt(cOli1,cOli2,cOli3,cOli4,?b,cOli4,cOli3,cOli2,cOli1,?a)
           - 3*cOlTt(cOli1,cOli2,cOli3,?b,cOli3,cOli2,cOli1,?a)*cA
           + 7/4*cOlTt(cOli1,cOli2,?b,cOli2,cOli1,?a)*cA^2
           - 1/12*cOlTt(cOli1,?b,cOli1,?a)*cA^3
           + cOlTt(cOli1,cOli2,?b,cOli3,cOli4,?a)*cOldA(cOli1,cOli2,cOli3,cOli4)
           + 2*cOlTt(cOli1,cOli2,cOli3,?b,cOli3,cOli4,cOlk1,?a)*f(cOli1,cOlk1,cOlk2)*f(cOli2,cOli4,cOlk2)
           + 2*cOlTt(cOli1,cOli2,cOli3,?b,cOli4,cOlk1,cOli1,?a)*f(cOli2,cOlk1,cOlk2)*f(cOli3,cOli4,cOlk2)
           - cOlTt(cOli1,cOli2,cOli3,?b,cOli4,cOlk1,?a)*f(cOli1,cOlk1,cOlk2)*f(cOli2,cOlk2,cOlk3)*f(cOli3,cOli4,cOlk3)*i_
           + cOlTt(cOli1,cOli2,?b,cOli3,cOli4,cOlk1,?a)*f(cOli1,cOlk1,cOlk2)*f(cOli2,cOli3,cOlk3)*f(cOli4,cOlk2,cOlk3)*i_
           - 11/6*cOlTt(cOli1,cOli2,?b,cOli3,cOli4,?a)*f(cOli1,cOli4,cOlk1)*f(cOli2,cOli3,cOlk1)*cA;
*        sum cOlk1,cOlk2,cOlk3;
        if ( count(cOldA,1) > 0 );
          #do isbb = 1,`RANK'
            if ( count(cOlpA`isbb',1) == 0 );
                id,once,cOldA(?a) = cOldA`isbb'(?a);
                ToVector,cOldA`isbb',cOlpA`isbb';
            endif;
          #enddo
        endif;
        id  cOlTt(cOli1?,cOli2?,cOli3?,?b,cOli1?,cOli2?,cOli3?,?a) =
         + 1/4*cOlTt(cOli1,?b,cOli1,?a)*cA^2
         - 3/2*cOlTt(cOli1,cOli2,?b,cOli2,cOli1,?a)*cA
         + cOlTt(cOli1,cOli2,?b,cOli3,cOlk4,?a)*f(cOli1,cOlk4,cOlk5)*f(cOli2,cOli3,cOlk5)
         + cOlTt(cOli1,cOli2,cOli3,?b,cOli3,cOli2,cOli1,?a);
        sum cOlk1,...,cOlk5;
      endif;
      id cOlTt(cOli1?,cOli2?,?b,cOli1?,cOli2?,?a) = cOlTt(cOli1,cOli2,?b,cOli2,cOli1,?a)
        -cA/2*cOlTt(cOli1,?b,cOli1,?a);
      ReplaceLoop,f,a=3,l<4,outfun=cOlff;
      id  cOlff(cOli1?,cOli2?) = -cA*d_(cOli1,cOli2);
      id  cOlff(cOli1?,cOli2?,cOli3?) = cA/2*f(cOli1,cOli2,cOli3);
    endrepeat;
    id cOlTt(cOli1?,cOli2?,cOli3?,?a)*f(cOli1?,cOli3?,cOli4?) =
        +i_*cOlTt(cOli1,cOlk1,?a)*f(cOli2,cOli3,cOlk1)*f(cOli1,cOli3,cOli4)
        +i_*cA/2*cOlTt(cOli4,cOli2,?a);
    sum cOlk1;
  endrepeat;
  id cOlTt(cOli1?,cOli2?,cOli3?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,cOli3,?a)
       -cOlTt(cOli1,cOlk2,?a)*f(cOli3,cOli1,cOlk1)*f(cOli2,cOlk1,cOlk2)
       -cA/2*cOlTt(cOli3,cOli2,?a);
  sum cOlk1,cOlk2;
endrepeat;
AB	cR,cA,[cR-cA/2];
#call SORT(color-3-1)
Keep Brackets;
repeat;
  repeat;
    repeat;
      repeat;
        repeat;
          repeat;
            id  cOlTt(cOli1?,cOli1?,?a)       = cR*cOlTt(?a);
            id  cOlTt(cOli1?,cOli2?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,?a);
            id  cOlTt(cOli1?,cOli2?,?a)*f(cOli1?,cOli2?,cOli3?) = i_*cA/2*cOlTt(cOli3,?a);
          endrepeat;
          id cOlTt = I2R*NA/cR;
          id cOlTt(cOli1?,cOli2?,?b,cOli1?,cOli2?,?a) = cOlTt(cOli1,cOli2,?b,cOli2,cOli1,?a)
              -cA/2*cOlTt(cOli1,?b,cOli1,?a);
          ReplaceLoop,f,a=3,l<4,outfun=cOlff;
          id  cOlff(cOli1?,cOli2?) = -cA*d_(cOli1,cOli2);
          id  cOlff(cOli1?,cOli2?,cOli3?) = cA/2*f(cOli1,cOli2,cOli3);
*          id f(cOli1?,cOli2?,cOli3?)*f(cOli1?,cOli2?,cOli4?) = cA*d_(cOli3,cOli4);
*          id f(cOli1?,cOli2?,cOlj1?)*f(cOli2?,cOli3?,cOlj2?)*f(cOli3?,cOli1?,cOlj3?) = cA/2*f(cOlj1,cOlj2,cOlj3);
        endrepeat;
        id cOlTt(cOli1?,cOli2?,cOli3?,?a)*f(cOli1?,cOli3?,cOli4?) =
            +i_*cOlTt(cOli1,cOlk1,?a)*f(cOli2,cOli3,cOlk1)*f(cOli1,cOli3,cOli4)
            +i_*cA/2*cOlTt(cOli4,cOli2,?a);
        sum cOlk1;
      endrepeat;
      id cOlTt(cOli1?,cOli2?,cOli3?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,cOli3,?a)
           -cOlTt(cOli1,cOlk2,?a)*f(cOli3,cOli1,cOlk1)*f(cOli2,cOlk1,cOlk2)
           -cA/2*cOlTt(cOli3,cOli2,?a);
      sum cOlk1,cOlk2;
    endrepeat;
    id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,?a)*f(cOli1?,cOli4?,cOli5?) =
        +i_*cA/2*cOlTt(cOli5,cOli2,cOli3,?a)
        +i_*cOlTt(cOli1,cOlk1,cOli3,?a)*f(cOli2,cOli4,cOlk1)*f(cOli1,cOli4,cOli5)
        +i_*cOlTt(cOli1,cOli2,cOlk1,?a)*f(cOli3,cOli4,cOlk1)*f(cOli1,cOli4,cOli5);
    sum cOlk1;
  endrepeat;
  id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,cOli3,cOli4,?a)
        +i_*cOlTt(cOli1,cOli2,cOli3,cOlk1,?a)*f(cOli4,cOli1,cOlk1)
        +i_*cOlTt(cOli1,cOli2,cOlk1,cOli4,?a)*f(cOli3,cOli1,cOlk1);
  sum cOlk1;
endrepeat;
AB	cR,cA,[cR-cA/2];
#call SORT(color-3-2)
Keep Brackets;
repeat;
  repeat;
    repeat;
      repeat;
        repeat;
          repeat;
            repeat;
              repeat;
                id  cOlTt(cOli1?,cOli1?,?a)   = cR*cOlTt(?a);
                id  cOlTt(cOli1?,cOli2?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,?a);
                id  cOlTt(cOli1?,cOli2?,?a)*f(cOli1?,cOli2?,cOli3?) = i_*cA/2*cOlTt(cOli3,?a);
              endrepeat;
              id cOlTt = I2R*NA/cR;
              id cOlTt(cOli1?,cOli2?,?b,cOli1?,cOli2?,?a) = cOlTt(cOli1,cOli2,?b,cOli2,cOli1,?a)
                  -cA/2*cOlTt(cOli1,?b,cOli1,?a);
              ReplaceLoop,f,a=3,l<4,outfun=cOlff;
              id  cOlff(cOli1?,cOli2?) = -cA*d_(cOli1,cOli2);
              id  cOlff(cOli1?,cOli2?,cOli3?) = cA/2*f(cOli1,cOli2,cOli3);
*              id f(cOli1?,cOli2?,cOli3?)*f(cOli1?,cOli2?,cOli4?) = cA*d_(cOli3,cOli4);
*              id f(cOli1?,cOli2?,cOlj1?)*f(cOli2?,cOli3?,cOlj2?)*f(cOli3?,cOli1?,cOlj3?) = cA/2*f(cOlj1,cOlj2,cOlj3);
            endrepeat;
            id cOlTt(cOli1?,cOli2?,cOli3?,?a)*f(cOli1?,cOli3?,cOli4?) =
                +i_*cOlTt(cOli1,cOlk1,?a)*f(cOli2,cOli3,cOlk1)*f(cOli1,cOli3,cOli4)
                +i_*cA/2*cOlTt(cOli4,cOli2,?a);
            sum cOlk1;
          endrepeat;
          id cOlTt(cOli1?,cOli2?,cOli3?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,cOli3,?a)
               -cOlTt(cOli1,cOlk2,?a)*f(cOli3,cOli1,cOlk1)*f(cOli2,cOlk1,cOlk2)
               -cA/2*cOlTt(cOli3,cOli2,?a);
          sum cOlk1,cOlk2;
        endrepeat;
        id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,?a)*f(cOli1?,cOli4?,cOli5?) =
            +i_*cA/2*cOlTt(cOli5,cOli2,cOli3,?a)
            +i_*cOlTt(cOli1,cOlk1,cOli3,?a)*f(cOli2,cOli4,cOlk1)*f(cOli1,cOli4,cOli5)
            +i_*cOlTt(cOli1,cOli2,cOlk1,?a)*f(cOli3,cOli4,cOlk1)*f(cOli1,cOli4,cOli5);
        sum cOlk1;
      endrepeat;
      id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,cOli3,cOli4,?a)
            +i_*cOlTt(cOli1,cOli2,cOli3,cOlk1,?a)*f(cOli4,cOli1,cOlk1)
            +i_*cOlTt(cOli1,cOli2,cOlk1,cOli4,?a)*f(cOli3,cOli1,cOlk1);
      sum cOlk1;
    endrepeat;
    id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,?a)*f(cOli1?,cOli5?,cOli6?) =
        +i_*cA/2*cOlTt(cOli6,cOli2,cOli3,cOli4,?a)
        +i_*cOlTt(cOli1,cOlk1,cOli3,cOli4,?a)*f(cOli2,cOli5,cOlk1)*f(cOli1,cOli5,cOli6)
        +i_*cOlTt(cOli1,cOli2,cOlk1,cOli4,?a)*f(cOli3,cOli5,cOlk1)*f(cOli1,cOli5,cOli6)
        +i_*cOlTt(cOli1,cOli2,cOli3,cOlk1,?a)*f(cOli4,cOli5,cOlk1)*f(cOli1,cOli5,cOli6);
    sum cOlk1;
  endrepeat;
  id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,cOli3,cOli4,cOli5,?a)
        +i_*cOlTt(cOli1,cOli2,cOli3,cOli4,cOlk1,?a)*f(cOli5,cOli1,cOlk1)
        +i_*cOlTt(cOli1,cOli2,cOli3,cOlk1,cOli5,?a)*f(cOli4,cOli1,cOlk1)
        +i_*cOlTt(cOli1,cOli2,cOlk1,cOli4,cOli5,?a)*f(cOli3,cOli1,cOlk1);
  sum cOlk1;
endrepeat;
AB	cR,cA,[cR-cA/2];
#call SORT(color-3-3)
Keep Brackets;
repeat;
  repeat;
    repeat;
      repeat;
        repeat;
          repeat;
            repeat;
              repeat;
                repeat;
                  repeat;
                    repeat;
                      repeat;
                        id  cOlTt(cOli1?,cOli1?,?a)   = cR*cOlTt(?a);
                        id  cOlTt(cOli1?,cOli2?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,?a);
                        id  cOlTt(cOli1?,cOli2?,?a)*f(cOli1?,cOli2?,cOli3?) = i_*cA/2*cOlTt(cOli3,?a);
                      endrepeat;
                      id cOlTt = I2R*NA/cR;
                      id cOlTt(cOli1?,cOli2?,?b,cOli1?,cOli2?,?a) = cOlTt(cOli1,cOli2,?b,cOli2,cOli1,?a)
                          -cA/2*cOlTt(cOli1,?b,cOli1,?a);
                      ReplaceLoop,f,a=3,l<4,outfun=cOlff;
                      id  cOlff(cOli1?,cOli2?) = -cA*d_(cOli1,cOli2);
                      id  cOlff(cOli1?,cOli2?,cOli3?) = cA/2*f(cOli1,cOli2,cOli3);
*                      id f(cOli1?,cOli2?,cOli3?)*f(cOli1?,cOli2?,cOli4?) = cA*d_(cOli3,cOli4);
*                      id f(cOli1?,cOli2?,cOlj1?)*f(cOli2?,cOli3?,cOlj2?)*f(cOli3?,cOli1?,cOlj3?) = cA/2*f(cOlj1,cOlj2,cOlj3);
                    endrepeat;
                    id cOlTt(cOli1?,cOli2?,cOli3?,?a)*f(cOli1?,cOli3?,cOli4?) =
                        +i_*cOlTt(cOli1,cOlk1,?a)*f(cOli2,cOli3,cOlk1)*f(cOli1,cOli3,cOli4)
                        +i_*cA/2*cOlTt(cOli4,cOli2,?a);
                    sum cOlk1;
                  endrepeat;
                  id cOlTt(cOli1?,cOli2?,cOli3?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,cOli3,?a)
                       -cOlTt(cOli1,cOlk2,?a)*f(cOli3,cOli1,cOlk1)*f(cOli2,cOlk1,cOlk2)
                       -cA/2*cOlTt(cOli3,cOli2,?a);
                  sum cOlk1,cOlk2;
                endrepeat;
                id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,?a)*f(cOli1?,cOli4?,cOli5?) =
                    +i_*cA/2*cOlTt(cOli5,cOli2,cOli3,?a)
                    +i_*cOlTt(cOli1,cOlk1,cOli3,?a)*f(cOli2,cOli4,cOlk1)*f(cOli1,cOli4,cOli5)
                    +i_*cOlTt(cOli1,cOli2,cOlk1,?a)*f(cOli3,cOli4,cOlk1)*f(cOli1,cOli4,cOli5);
                sum cOlk1;
              endrepeat;
              id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,cOli3,cOli4,?a)
                    +i_*cOlTt(cOli1,cOli2,cOli3,cOlk1,?a)*f(cOli4,cOli1,cOlk1)
                    +i_*cOlTt(cOli1,cOli2,cOlk1,cOli4,?a)*f(cOli3,cOli1,cOlk1);
              sum cOlk1;
            endrepeat;
            id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,?a)*f(cOli1?,cOli5?,cOli6?) =
                +i_*cA/2*cOlTt(cOli6,cOli2,cOli3,cOli4,?a)
                +i_*cOlTt(cOli1,cOlk1,cOli3,cOli4,?a)*f(cOli2,cOli5,cOlk1)*f(cOli1,cOli5,cOli6)
                +i_*cOlTt(cOli1,cOli2,cOlk1,cOli4,?a)*f(cOli3,cOli5,cOlk1)*f(cOli1,cOli5,cOli6)
                +i_*cOlTt(cOli1,cOli2,cOli3,cOlk1,?a)*f(cOli4,cOli5,cOlk1)*f(cOli1,cOli5,cOli6);
            sum cOlk1;
          endrepeat;
          id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,cOli3,cOli4,cOli5,?a)
                +i_*cOlTt(cOli1,cOli2,cOli3,cOli4,cOlk1,?a)*f(cOli5,cOli1,cOlk1)
                +i_*cOlTt(cOli1,cOli2,cOli3,cOlk1,cOli5,?a)*f(cOli4,cOli1,cOlk1)
                +i_*cOlTt(cOli1,cOli2,cOlk1,cOli4,cOli5,?a)*f(cOli3,cOli1,cOlk1);
          sum cOlk1;
        endrepeat;
        id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?,?a)*f(cOli1?,cOli6?,cOli7?) =
            +i_*cA/2*cOlTt(cOli7,cOli2,cOli3,cOli4,cOli5,?a)
            +i_*cOlTt(cOli1,cOlk1,cOli3,cOli4,cOli5,?a)*f(cOli2,cOli6,cOlk1)*f(cOli1,cOli6,cOli7)
            +i_*cOlTt(cOli1,cOli2,cOlk1,cOli4,cOli5,?a)*f(cOli3,cOli6,cOlk1)*f(cOli1,cOli6,cOli7)
            +i_*cOlTt(cOli1,cOli2,cOli3,cOlk1,cOli5,?a)*f(cOli4,cOli6,cOlk1)*f(cOli1,cOli6,cOli7)
            +i_*cOlTt(cOli1,cOli2,cOli3,cOli4,cOlk1,?a)*f(cOli5,cOli6,cOlk1)*f(cOli1,cOli6,cOli7);
        sum cOlk1;
      endrepeat;
      id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?,cOli1?,?a) = [cR-cA/2]*cOlTt(cOli2,cOli3,cOli4,cOli5,cOli6,?a)
            +i_*cOlTt(cOli1,cOli2,cOli3,cOli4,cOli5,cOlk1,?a)*f(cOli6,cOli1,cOlk1)
            +i_*cOlTt(cOli1,cOli2,cOli3,cOli4,cOlk1,cOli6,?a)*f(cOli5,cOli1,cOlk1)
            +i_*cOlTt(cOli1,cOli2,cOli3,cOlk1,cOli5,cOli6,?a)*f(cOli4,cOli1,cOlk1)
            +i_*cOlTt(cOli1,cOli2,cOlk1,cOli4,cOli5,cOli6,?a)*f(cOli3,cOli1,cOlk1);
      sum cOlk1;
    endrepeat;
    id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?,cOli7?,?a)*f(cOli1?,cOli7?,cOli8?) =
        +i_*cA/2*cOlTt(cOli8,cOli2,cOli3,cOli4,cOli5,cOli6,?a)
        +i_*cOlTt(cOli1,cOlk1,cOli3,cOli4,cOli5,cOli6,?a)*f(cOli2,cOli7,cOlk1)*f(cOli1,cOli7,cOli8)
        +i_*cOlTt(cOli1,cOli2,cOlk1,cOli4,cOli5,cOli6,?a)*f(cOli3,cOli7,cOlk1)*f(cOli1,cOli7,cOli8)
        +i_*cOlTt(cOli1,cOli2,cOli3,cOlk1,cOli5,cOli6,?a)*f(cOli4,cOli7,cOlk1)*f(cOli1,cOli7,cOli8)
        +i_*cOlTt(cOli1,cOli2,cOli3,cOli4,cOlk1,cOli6,?a)*f(cOli5,cOli7,cOlk1)*f(cOli1,cOli7,cOli8)
        +i_*cOlTt(cOli1,cOli2,cOli3,cOli4,cOli5,cOlk1,?a)*f(cOli6,cOli7,cOlk1)*f(cOli1,cOli7,cOli8);
    sum cOlk1;
  endrepeat;
  id cOlTt(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?,cOli7?,cOli1?,?a) =
        +[cR-cA/2]*cOlTt(cOli2,cOli3,cOli4,cOli5,cOli6,cOli7,?a)
        -cOlTt(cOli1,cOli2,cOli3,cOli4,cOli5,cOlk2,?a)*f(cOli6,cOlk1,cOlk2)*f(cOli7,cOli1,cOlk1)
        -cOlTt(cOli1,cOli2,cOli3,cOli4,cOlk2,cOli6,?a)*f(cOli5,cOlk1,cOlk2)*f(cOli7,cOli1,cOlk1)
        -cOlTt(cOli1,cOli2,cOli3,cOli4,cOlk2,cOli7,?a)*f(cOli5,cOlk1,cOlk2)*f(cOli6,cOli1,cOlk1)
        -cOlTt(cOli1,cOli2,cOli3,cOlk2,cOli5,cOli6,?a)*f(cOli4,cOlk1,cOlk2)*f(cOli7,cOli1,cOlk1)
        -cOlTt(cOli1,cOli2,cOli3,cOlk2,cOli5,cOli7,?a)*f(cOli4,cOlk1,cOlk2)*f(cOli6,cOli1,cOlk1)
        -cOlTt(cOli1,cOli2,cOli3,cOlk2,cOli6,cOli7,?a)*f(cOli4,cOlk1,cOlk2)*f(cOli5,cOli1,cOlk1)
        -cOlTt(cOli1,cOli2,cOlk2,cOli4,cOli5,cOli6,?a)*f(cOli3,cOlk1,cOlk2)*f(cOli7,cOli1,cOlk1)
        -cOlTt(cOli1,cOli2,cOlk2,cOli4,cOli5,cOli7,?a)*f(cOli3,cOlk1,cOlk2)*f(cOli6,cOli1,cOlk1)
        -cOlTt(cOli1,cOli2,cOlk2,cOli4,cOli6,cOli7,?a)*f(cOli3,cOlk1,cOlk2)*f(cOli5,cOli1,cOlk1)
        -cOlTt(cOli1,cOli2,cOlk2,cOli5,cOli6,cOli7,?a)*f(cOli3,cOlk1,cOlk2)*f(cOli4,cOli1,cOlk1)
        -cOlTt(cOli1,cOlk2,cOli3,cOli4,cOli5,cOli6,?a)*f(cOli2,cOlk1,cOlk2)*f(cOli7,cOli1,cOlk1)
        -cOlTt(cOli1,cOlk2,cOli3,cOli4,cOli5,cOli7,?a)*f(cOli2,cOlk1,cOlk2)*f(cOli6,cOli1,cOlk1)
        -cOlTt(cOli1,cOlk2,cOli3,cOli4,cOli6,cOli7,?a)*f(cOli2,cOlk1,cOlk2)*f(cOli5,cOli1,cOlk1)
        -cOlTt(cOli1,cOlk2,cOli3,cOli5,cOli6,cOli7,?a)*f(cOli2,cOlk1,cOlk2)*f(cOli4,cOli1,cOlk1)
        -cOlTt(cOli1,cOlk2,cOli4,cOli5,cOli6,cOli7,?a)*f(cOli2,cOlk1,cOlk2)*f(cOli3,cOli1,cOlk1)
        -cA/2*cOlTt(cOli7,cOli2,cOli3,cOli4,cOli5,cOli6,?a)
        -cA/2*cOlTt(cOli6,cOli2,cOli3,cOli4,cOli5,cOli7,?a)
        -cA/2*cOlTt(cOli5,cOli2,cOli3,cOli4,cOli6,cOli7,?a)
        -cA/2*cOlTt(cOli4,cOli2,cOli3,cOli5,cOli6,cOli7,?a)
        -cA/2*cOlTt(cOli3,cOli2,cOli4,cOli5,cOli6,cOli7,?a);
  sum cOlk1,cOlk2;
endrepeat;
AB	cR,cA,[cR-cA/2];
#call SORT(color-3-4)
#ifndef `ALTERNATEMETHOD'
Keep brackets;
repeat;
	if ( count(cOlff,1) == 0 );
		ReplaceLoop,f,a=3,l=all,outfun=cOlff;
		id	cOlff(cOli1?,cOli2?) = -cA*d_(cOli1,cOli2);
		id	cOlff(cOli1?,cOli2?,cOli3?) = cA/2*f(cOli1,cOli2,cOli3);
	endif;
endrepeat;
if ( count(cOlff,1) ) redefine ik1c "0";
#call adjoint
#endif
AB	cR,cA,[cR-cA/2];
#call SORT(color-4)
Keep Brackets;
#enddo
*
*   Now we eliminate the Trace cOlTt. It has only different indices now!
*   There is still a possible simplification in this algorithm when
*   there is already a cOldR which is symmetric. If it has more than one
*   index common with our cOlTt, there could be shortcuts.
*   These are exploited by writing cOldR(cOli1,...,in) = cOlpR(cOli1)*...*cOlpR(in)
*   The vector has an extra index to keep the different cOldR apart.
*
id  cOlTt(cOli1?) = 0;
id  cOlTt(cOli1?,cOli2?) = I2R*d_(cOli1,cOli2);
id  cOlTt(cOli1?,cOli2?,cOli3?) = cOldR(cOli1,cOli2,cOli3)+i_/2*f(cOli1,cOli2,cOli3)*I2R;
id  cOlTt(cOli1?,cOli2?,cOli3?,cOli4?) = cOldR(cOli1,cOli2,cOli3,cOli4)
    +1/2*i_*(cOldR(cOli1,cOli2,cOlk)*f(cOli3,cOli4,cOlk)+cOldR(cOli3,cOli4,cOlk)*f(cOli1,cOli2,cOlk))
    -1/6*f(cOli1,cOli3,cOlk)*f(cOli2,cOli4,cOlk)*I2R+1/3*f(cOli1,cOli4,cOlk)*f(cOli2,cOli3,cOlk)*I2R;

id  cOlTt(?a) = T(?a);
id  T(cOli1?,cOli2?,?a) = cOlE0(cOli1,cOli2)*T(?a)+cOlE0(cOlk)*i_*f(cOli1,cOli2,cOlk)*T(?a)/2;
sum cOlk;
repeat;
id  cOlE0(?a)*T(cOli1?,?b) = cOlE0(?a,cOli1)*T(?b)
        +sum_(cOlx,1,nargs_(?a),Bernoulli_(cOlx)*cOlE(cOlx,?a,cOli1))*T(?b);
repeat;
    id  cOlE(cOlx?pos_,?a,cOli1?) = distrib_(1,1,cOlEa,cOlEb,?a)*cOlEc(cOlx-1,cOli1,cOlk);
    id  cOlEa(cOli1?)*cOlEb(?a)*cOlEc(cOlx?,cOli2?,cOli3?) = cOlE(cOlx,?a,cOli3)*i_*f(cOli1,cOli2,cOli3);
    sum cOlk;
endrepeat;
id  cOlE(0,?a) = cOlE0(?a);
id  T = 1;
if ( match(T(cOli1?)) );
    id  cOlE0(?a)*T(cOli1?) = cOldR(?a,cOli1);
elseif ( match(T(cOli1?,cOli2?)) );
    id  cOlE0(cOli1?)*T(cOli2?,cOli3?) = cOldR(cOli1,cOli2,cOli3)+i_/2*f(cOli1,cOli2,cOli3)*I2R;
    id  cOlE0(cOli1?,cOli2?)*T(cOli3?,cOli4?) = cOldR(cOli1,cOli2,cOli3,cOli4)
        +i_/2*f(cOli3,cOli4,cOlk)*cOldR(cOli1,cOli2,cOlk)
        +I2R*(f(cOli1,cOli3,cOlk)*f(cOli2,cOli4,cOlk)+f(cOli1,cOli4,cOlk)*f(cOli2,cOli3,cOlk))/12;
    sum cOlk;
endif;
endrepeat;
id  cOldR(cOli1?) = 0;
id  cOldR(cOli1?,cOli2?) = I2R*d_(cOli1,cOli2);
AB	cR,cA,[cR-cA/2];
#call SORT(color-5)
Keep Brackets;
if ( count(cOldR,1) );
#do ik1d = 1,`RANK'
    if ( count(cOlpR`ik1d',1) == 0 );
        id,once,cOldR(?a) = cOldR`ik1d'(?a);
        ToVector,cOldR`ik1d',cOlpR`ik1d';
    endif;
#enddo
endif;
AB	cR,cA,[cR-cA/2];
#call SORT(color-6)
Repeat;
    ReplaceLoop,f,argument=3,loopsize<4,outfun=cOlff;
    id cOlff(cOli1?,cOli2?) = -cA*d_(cOli1,cOli2);
    id cOlff(cOli1?,cOli2?,cOli3?) = cA/2*f(cOli1,cOli2,cOli3);
EndRepeat;
#do isimpli = 1,`RANK'
    if ( count(cOlpR`isimpli',1) == 3 )
        id f(cOlpR`isimpli',cOli1?,cOli3?)*f(cOlpR`isimpli',cOli2?,cOli3?) =
            cOlpR`isimpli'(cOli1)*cOlpR`isimpli'(cOli2)*cA/2;
#enddo
#enddo
*
* At this point we have eliminated the R-traces. We are left with the
* traces in the adjoint representation.
*
#endif
id	[cR-cA/2] = cR-cA/2;
#endprocedure
*
*--#] color : 
*--#[ adjoint :
*
#procedure adjoint
*
*	Procedure to deal with gluonic loops (adjoint representation)
*	In this case there are special shortcuts for odd loops.
*	Also even loops have special savings.
*	Use the declarations of the file cfactor.h
*	Do not use indices cOlk,cOlk1,cOlk2,cOlk3,cOlk4,cOlk5 when calling this routine!
*
*	Routine by J.Vermaseren 24-may-1997
*
#define adj "0"
repeat;
	if ( count(cOlff,1) == 0 );
		ReplaceLoop,f,a=3,l=all,outfun=cOlff;
		id	cOlff(cOli1?,cOli2?) = -cA*d_(cOli1,cOli2);
		id	cOlff(cOli1?,cOli2?,cOli3?) = cA/2*f(cOli1,cOli2,cOli3);
	endif;
endrepeat;
if ( count(cOlff,1) ) redefine adj "1";
renumber;
#call SORT(adjoint-1)
#if `adj' > 0
#do iStageB = 1,1
	id,once,cOlff(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?,cOli7?) = 1/2*(
		+cOlff(cOlk1,cOli6,cOli5,cOli4,cOli3,cOli2)*f(cOli1,cOli7,cOlk1)
		+cOlff(cOlk1,cOli5,cOli4,cOli3,cOli2,cOli7)*f(cOli1,cOli6,cOlk1)
		+cOlff(cOli1,cOli5,cOli4,cOli3,cOli2,cOlk1)*f(cOli7,cOli6,cOlk1)
		+cOlff(cOli1,cOlk1,cOli3,cOli2,cOli6,cOli7)*f(cOli5,cOli4,cOlk1)
		+cOlff(cOli1,cOli4,cOlk1,cOli2,cOli6,cOli7)*f(cOli5,cOli3,cOlk1)
		+cOlff(cOli1,cOli4,cOli3,cOlk1,cOli6,cOli7)*f(cOli5,cOli2,cOlk1)
		+cOlff(cOli1,cOlk1,cOli2,cOli5,cOli6,cOli7)*f(cOli4,cOli3,cOlk1)
		+cOlff(cOli1,cOli3,cOlk1,cOli5,cOli6,cOli7)*f(cOli4,cOli2,cOlk1)
		+cOlff(cOli1,cOlk1,cOli4,cOli5,cOli6,cOli7)*f(cOli3,cOli2,cOlk1)
	);
#call SORT(adjoint-2-a)
	id,once,cOlff(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?) = -cOldA(cOli1,cOli2,cOli3,cOli4,cOli5,cOli6)
       - 1/20*cOlff(cOli1,cOli2,cOli3,cOli4,cOlk2)*f(cOli5,cOli6,cOlk2)
       - 1/20*cOlff(cOli1,cOli2,cOli3,cOli5,cOlk2)*f(cOli4,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli2,cOli3,cOlk2,cOli4)*f(cOli5,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli2,cOli3,cOlk2,cOli5)*f(cOli4,cOli6,cOlk2)
       - 1/3*cOlff(cOli1,cOli2,cOli3,cOlk2,cOli6)*f(cOli4,cOli5,cOlk2)
       - 1/20*cOlff(cOli1,cOli2,cOli4,cOli3,cOlk2)*f(cOli5,cOli6,cOlk2)
       - 1/20*cOlff(cOli1,cOli2,cOli4,cOli5,cOlk2)*f(cOli3,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli2,cOli4,cOlk2,cOli3)*f(cOli5,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli2,cOli4,cOlk2,cOli5)*f(cOli3,cOli6,cOlk2)
       - 7/30*cOlff(cOli1,cOli2,cOli4,cOlk2,cOli6)*f(cOli3,cOli5,cOlk2)
       - 1/20*cOlff(cOli1,cOli2,cOli5,cOli3,cOlk2)*f(cOli4,cOli6,cOlk2)
       - 1/20*cOlff(cOli1,cOli2,cOli5,cOli4,cOlk2)*f(cOli3,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli2,cOli5,cOlk2,cOli3)*f(cOli4,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli2,cOli5,cOlk2,cOli4)*f(cOli3,cOli6,cOlk2)
       - 1/60*cOlff(cOli1,cOli2,cOlk2,cOli3,cOli4)*f(cOli5,cOli6,cOlk2)
       - 1/60*cOlff(cOli1,cOli2,cOlk2,cOli3,cOli5)*f(cOli4,cOli6,cOlk2)
       - 7/60*cOlff(cOli1,cOli2,cOlk2,cOli3,cOli6)*f(cOli4,cOli5,cOlk2)
       - 1/60*cOlff(cOli1,cOli2,cOlk2,cOli4,cOli3)*f(cOli5,cOli6,cOlk2)
       - 1/60*cOlff(cOli1,cOli2,cOlk2,cOli4,cOli5)*f(cOli3,cOli6,cOlk2)
       - 7/60*cOlff(cOli1,cOli2,cOlk2,cOli4,cOli6)*f(cOli3,cOli5,cOlk2)
       - 1/60*cOlff(cOli1,cOli2,cOlk2,cOli5,cOli3)*f(cOli4,cOli6,cOlk2)
       - 1/60*cOlff(cOli1,cOli2,cOlk2,cOli5,cOli4)*f(cOli3,cOli6,cOlk2)
       - 9/20*cOlff(cOli1,cOli2,cOlk2,cOli5,cOli6)*f(cOli3,cOli4,cOlk2)
       - 1/20*cOlff(cOli1,cOli3,cOli2,cOli4,cOlk2)*f(cOli5,cOli6,cOlk2)
       - 1/20*cOlff(cOli1,cOli3,cOli2,cOli5,cOlk2)*f(cOli4,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli3,cOli2,cOlk2,cOli4)*f(cOli5,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli3,cOli2,cOlk2,cOli5)*f(cOli4,cOli6,cOlk2)
       - 1/20*cOlff(cOli1,cOli3,cOli4,cOli2,cOlk2)*f(cOli5,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli3,cOli4,cOlk2,cOli5)*f(cOli2,cOli6,cOlk2)
       - 1/60*cOlff(cOli1,cOli3,cOli4,cOlk2,cOli6)*f(cOli2,cOli5,cOlk2)
       - 1/20*cOlff(cOli1,cOli3,cOli5,cOli2,cOlk2)*f(cOli4,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli3,cOli5,cOlk2,cOli4)*f(cOli2,cOli6,cOlk2)
       - 1/60*cOlff(cOli1,cOli3,cOli5,cOlk2,cOli6)*f(cOli2,cOli4,cOlk2)
       - 1/60*cOlff(cOli1,cOli3,cOlk2,cOli2,cOli4)*f(cOli5,cOli6,cOlk2)
       - 1/60*cOlff(cOli1,cOli3,cOlk2,cOli2,cOli5)*f(cOli4,cOli6,cOlk2)
       - 1/60*cOlff(cOli1,cOli3,cOlk2,cOli4,cOli5)*f(cOli2,cOli6,cOlk2)
       - 1/12*cOlff(cOli1,cOli3,cOlk2,cOli4,cOli6)*f(cOli2,cOli5,cOlk2)
       - 1/60*cOlff(cOli1,cOli3,cOlk2,cOli5,cOli4)*f(cOli2,cOli6,cOlk2)
       - 1/12*cOlff(cOli1,cOli3,cOlk2,cOli5,cOli6)*f(cOli2,cOli4,cOlk2)
       - 1/20*cOlff(cOli1,cOli4,cOli2,cOli3,cOlk2)*f(cOli5,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli4,cOli2,cOlk2,cOli5)*f(cOli3,cOli6,cOlk2)
       - 1/20*cOlff(cOli1,cOli4,cOli3,cOli2,cOlk2)*f(cOli5,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli4,cOli3,cOlk2,cOli5)*f(cOli2,cOli6,cOlk2)
       - 1/60*cOlff(cOli1,cOli4,cOli3,cOlk2,cOli6)*f(cOli2,cOli5,cOlk2)
       - 1/60*cOlff(cOli1,cOli4,cOli5,cOlk2,cOli6)*f(cOli2,cOli3,cOlk2)
       - 1/60*cOlff(cOli1,cOli4,cOlk2,cOli2,cOli5)*f(cOli3,cOli6,cOlk2)
       - 1/60*cOlff(cOli1,cOli4,cOlk2,cOli3,cOli5)*f(cOli2,cOli6,cOlk2)
       - 1/30*cOlff(cOli1,cOli4,cOlk2,cOli3,cOli6)*f(cOli2,cOli5,cOlk2)
       - 1/12*cOlff(cOli1,cOli4,cOlk2,cOli5,cOli6)*f(cOli2,cOli3,cOlk2)
       - 1/60*cOlff(cOli1,cOli5,cOli3,cOlk2,cOli6)*f(cOli2,cOli4,cOlk2)
       - 1/60*cOlff(cOli1,cOli5,cOli4,cOlk2,cOli6)*f(cOli2,cOli3,cOlk2)
       - 1/30*cOlff(cOli1,cOli5,cOlk2,cOli3,cOli6)*f(cOli2,cOli4,cOlk2)
       - 1/30*cOlff(cOli1,cOli5,cOlk2,cOli4,cOli6)*f(cOli2,cOli3,cOlk2)
       - 1/20*cOlff(cOli1,cOlk2,cOli3,cOli4,cOli6)*f(cOli2,cOli5,cOlk2)
       - 3/20*cOlff(cOli1,cOlk2,cOli3,cOli5,cOli6)*f(cOli2,cOli4,cOlk2)
       - 1/20*cOlff(cOli1,cOlk2,cOli4,cOli3,cOli6)*f(cOli2,cOli5,cOlk2)
       - 3/20*cOlff(cOli1,cOlk2,cOli4,cOli5,cOli6)*f(cOli2,cOli3,cOlk2)
       - 1/20*cOlff(cOli1,cOlk2,cOli5,cOli3,cOli6)*f(cOli2,cOli4,cOlk2)
       - 3/20*cOlff(cOli1,cOlk2,cOli5,cOli4,cOli6)*f(cOli2,cOli3,cOlk2);
#call SORT(adjoint-2-b)
id,once,cOlff(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?) = 
		+1/2*cOldA(cOli2,cOli3,cOli4,cOlk3)*f(cOlk3,cOli1,cOli5)
		-1/2*cOldA(cOli1,cOli4,cOli5,cOlk3)*f(cOlk3,cOli2,cOli3)
		-1/2*cOldA(cOli1,cOli3,cOli5,cOlk3)*f(cOlk3,cOli2,cOli4)
		-1/2*cOldA(cOli1,cOli2,cOli5,cOlk3)*f(cOlk3,cOli3,cOli4)
       + 1/12*f(cOli1,cOlk3,cOlk4)*f(cOli2,cOli3,cOlk3)*f(cOli4,cOli5,cOlk4)*cA
       + 1/12*f(cOli1,cOlk3,cOlk4)*f(cOli2,cOli5,cOlk4)*f(cOli3,cOli4,cOlk3)*cA
       + 1/12*f(cOli1,cOli3,cOlk3)*f(cOli2,cOli4,cOlk4)*f(cOli5,cOlk3,cOlk4)*cA
       - 1/6*f(cOli1,cOli5,cOlk3)*f(cOli2,cOli3,cOlk4)*f(cOli4,cOlk3,cOlk4)*cA
       + 1/12*f(cOli1,cOli5,cOlk3)*f(cOli2,cOli4,cOlk4)*f(cOli3,cOlk3,cOlk4)*cA;
id,once,cOlff(cOli1?,cOli2?,cOli3?,cOli4?) = cOldA(cOli1,cOli2,cOli3,cOli4)
		+cA*f(cOli1,cOli2,cOlk5)*f(cOli4,cOli3,cOlk5)/6
		+cA*f(cOli1,cOlk5,cOli4)*f(cOli3,cOli2,cOlk5)/6;
sum cOlk1,cOlk2,cOlk3,cOlk4,cOlk5;
if ( count(cOlff,1) );
	id  cOlff(?a) = T(?a);
	id  T(cOli1?,cOli2?,?a) = -cOlE0(cOli1,cOli2)*T(?a)-cOlE0(cOlk)*i_*f(cOli1,cOli2,cOlk)*T(?a)/2;
	sum cOlk;
	repeat;
	id  cOlE0(?a)*T(cOli1?,?b) = i_*cOlE0(?a,cOli1)*T(?b)
        +i_*sum_(cOlx,1,nargs_(?a),Bernoulli_(cOlx)*cOlE(cOlx,?a,cOli1))*T(?b);
	repeat;
    	id  cOlE(cOlx?pos_,?a,cOli1?) = distrib_(1,1,cOlEa,cOlEb,?a)*cOlEc(cOlx-1,cOli1,cOlk);
	    id  cOlEa(cOli1?)*cOlEb(?a)*cOlEc(cOlx?,cOli2?,cOli3?) = cOlE(cOlx,?a,cOli3)*i_*f(cOli1,cOli2,cOli3);
    	sum cOlk;
	endrepeat;
	id  cOlE(0,?a) = cOlE0(?a);
	id  T = 1;
	if ( match(T(cOli1?)) );
    	id  cOlE0(?a)*T(cOli1?) = i_*cOldA(?a,cOli1)*cOlacc(1-sign_(nargs_(?a)))/2;
		id	cOlacc(cOlx?) = cOlx;
	elseif ( match(T(cOli1?,cOli2?)) );
    	id  cOlE0(cOli1?)*T(cOli2?,cOli3?) = -i_*cA/2*f(cOli1,cOli2,cOli3);
	    id  cOlE0(cOli1?,cOli2?)*T(cOli3?,cOli4?) = -cOldA(cOli1,cOli2,cOli3,cOli4)
    	    -cA*(f(cOli1,cOli3,cOlk)*f(cOli2,cOli4,cOlk)+f(cOli1,cOli4,cOlk)*f(cOli2,cOli3,cOlk))/12;
	    sum cOlk;
	endif;
	endrepeat;
	id  cOldA(cOli1?) = 0;
	id  cOldA(cOli1?,cOli2?) = cA*d_(cOli1,cOli2);
endif;
#call SORT(adjoint-3)
if ( count(cOldA,1) > 0 );
#do isbb = 1,`RANK'
	if ( count(cOlpA`isbb',1) == 0 );
		id,once,cOldA(?a) = cOldA`isbb'(?a);
		ToVector,cOldA`isbb',cOlpA`isbb';
	endif;
#enddo
endif;
repeat;
	if ( count(cOlff,1) == 0 );
		ReplaceLoop,f,a=3,l=all,outfun=cOlff;
		id	cOlff(cOli1?,cOli2?) = -cA*d_(cOli1,cOli2);
		id	cOlff(cOli1?,cOli2?,cOli3?) = cA/2*f(cOli1,cOli2,cOli3);
	endif;
endrepeat;
if ( count(cOlff,1) ) redefine iStageB "0";
#call SORT(adjoint-4)
#enddo
#endif
#endprocedure
*
*--#] adjoint : 
*--#[ simpli :
*
#procedure simpli
*
*	Procedure tries to eliminate f tensors in an environment of invariants.
*	The strategy is:
*	Look for d1(cOli1,cOli2,...)*d2(cOli1,cOli3,...)*f(cOli1,cOli2,cOli3)
*	Take the two d1,d2 with the largest number of common indices.
*	Apply the generalized Jacobi identity for the d that has most
*	indices contracted with an f.
*	If such a construction is not present, try with common indices.
*	Take the d with the largest number of contractions with an f.
*	We do everything twice because the second time we choose in case
*	of a tie the other d.
*	Thus far it reduces everything up to 14 vertices and the majority
*	of terms with 16 vertices.
*
*	Made by J.Vermaseren, 24-may-1997
*
if ( count(f,1) != multipleof(2) ) discard;
#call contract
#call SORT(simpli-0)
#do isimpli = 1,`RANK'
	if ( count(cOlpR`isimpli',1) == 3 )
		id f(cOlpR`isimpli',cOli1?,cOli3?)*f(cOlpR`isimpli',cOli2?,cOli3?) =
			cOlpR`isimpli'(cOli1)*cOlpR`isimpli'(cOli2)*cA/2;
#enddo
#call d2f1

#call makeds
#define ftodo "0"
if ( count(f,1) ) redefine ftodo "1";
#call SORT(simpli-1)

#if `ftodo' > 0
#do ireduce = 1,6
#call dddff
renumber;
#call SORT(simpli-`ireduce'-1)
#do j = 1,2
if ( match(f(cOlp1?,cOlp2?,cOli1?)*cOlp1?.cOlp2?) );
	repeat id,once,f(cOlp1?,cOlp2?,cOli1?)*cOlp1?.cOlp2?^cOlx?pos_ = f(cOlp1,cOlp2,cOli1)*cOldd(cOlp1,cOlp2,cOlx);
	id	cOldd(cOlp1?,cOlp2?,1) = cOldd(cOlp1,cOlp2);
	if ( match(cOldd(cOlp1?,cOlp2?,cOlx?)) );
		id	cOldd(cOlp1?,cOlp2?) = cOldd(cOlp1,cOlp2,1);
		repeat id	cOldd(cOlp1?,cOlp2?,cOlx1?)*cOldd(cOlp3?,cOlp4?,cOlx2?) =
			+theta_(cOlx1-cOlx2)*cOldd(cOlp1,cOlp2,cOlx1)*cOlp3.cOlp4^cOlx2
			+theta_(cOlx2-cOlx1-1)*cOldd(cOlp3,cOlp4,cOlx2)*cOlp1.cOlp2^cOlx1;
	else;
		repeat;
			id,once,cOldd(cOlp1?,cOlp2?) = cOlddd(cOlp1,cOlp2);
			repeat id	cOlddd(cOlp1?,cOlp2?)*f(cOlp1?,cOli1?,cOli2?) = cOlddd(cOlp1,cOlp2)*cOlf1(cOlp1,cOli1,cOli2);
			id	cOlf1(cOlp1?,cOli1?,cOli2?) = cOlx1*f(cOlp1,cOli1,cOli2);
			repeat id	cOlddd(cOlp1?,cOlp2?)*f(cOlp2?,cOli1?,cOli2?) = cOlddd(cOlp1,cOlp2)*cOlf1(cOlp2,cOli1,cOli2);
			id	cOlf1(cOlp1?,cOli1?,cOli2?) = cOlx2*f(cOlp1,cOli1,cOli2);
			id	cOlddd(cOlp1?,cOlp2?)*cOlx1^cOly1?*cOlx2^cOly2? = cOldd(cOlp1,cOlp2,cOly1,cOly2);
		endrepeat;
		id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?) = theta_(cOlx1-cOlx2)*cOldd(cOlp1,cOlp2,cOlx1,cOlx1+cOlx2)
				+theta_(cOlx2-cOlx1-1)*cOldd(cOlp2,cOlp1,cOlx2,cOlx1+cOlx2);
		repeat;
			id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?)*cOldd(cOlp3?,cOlp4?,cOlx3?,cOlx4?) =
				+theta_(cOlx1-cOlx3-1)*cOldd(cOlp1,cOlp2,cOlx1,cOlx2)*cOlp3.cOlp4
				+theta_(cOlx3-cOlx1-1)*cOldd(cOlp3,cOlp4,cOlx3,cOlx4)*cOlp1.cOlp2
				+delta_(cOlx1-cOlx3)*theta_(cOlx2-cOlx4)*cOldd(cOlp1,cOlp2,cOlx1,cOlx2)*cOlp3.cOlp4
				+delta_(cOlx1-cOlx3)*theta_(cOlx4-cOlx2-1)*cOldd(cOlp3,cOlp4,cOlx3,cOlx4)*cOlp1.cOlp2;
		endrepeat;
		id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?) = cOldd(cOlp1,cOlp2,1);
	endif;
	repeat;
		id	cOldd(cOlp1?,cOlp2?,cOlx?)*cOlp1?.cOlp3? = cOldd(cOlp1,cOlp2,cOlx)*cOldA1(cOlp3);
		id	cOldd(cOlp1?,cOlp2?,cOlx?)*f(cOlp1?,cOli1?,cOli2?) = cOldd(cOlp1,cOlp2,cOlx)*cOldA1(cOlk)*f(cOlk,cOli1,cOli2);
		sum cOlk;
	endrepeat;
	repeat id cOldA1(?a)*cOldA1(?b) = cOldA1(?a,?b);
	id	cOldA1(?a) = cOlda1(?a);
	id	cOlda1(cOli1?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) = 0;
	id	cOlda1(cOli1?,cOli2?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) =
		-cOlda1(cOli1,cOlp2)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1);
	id	cOlda1(cOli1?,cOli2?,cOli3?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) =
		-cOlda1(cOli1,cOlp2,cOli3)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOlp2)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1);
	id	cOlda1(cOli1?,cOli2?,cOli3?,cOli4?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) =
		-cOlda1(cOli1,cOlp2,cOli3,cOli4)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOlp2,cOli4)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOlp2)*f(cOli1,cOli4,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1);
	id	cOlda1(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) =
		-cOlda1(cOli1,cOlp2,cOli3,cOli4,cOli5)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOlp2,cOli4,cOli5)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOlp2,cOli5)*f(cOli1,cOli4,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOli4,cOlp2)*f(cOli1,cOli5,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1);
	id	cOlda1(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) =
		-cOlda1(cOli1,cOlp2,cOli3,cOli4,cOli5,cOli6)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOlp2,cOli4,cOli5,cOli6)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOlp2,cOli5,cOli6)*f(cOli1,cOli4,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOli4,cOlp2,cOli6)*f(cOli1,cOli5,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOli4,cOli5,cOlp2)*f(cOli1,cOli6,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1);
	Multiply replace_(cOlda1,cOldA1);
	repeat id cOldA1(cOli1?,cOli2?,?a)*cOldd(cOlp1?,cOlp2?,cOlx?) = cOlp1(cOli1)*cOldA1(cOli2,?a)*cOldd(cOlp1,cOlp2,cOlx);
	id	cOldA1(cOli1?)*cOldd(cOlp1?,cOlp2?,cOlx?) = cOlp1(cOli1)*cOldd(cOlp1,cOlp2,cOlx);
	id	cOldd(cOlp1?,cOlp2?,cOlx?) = cOlp1.cOlp2^cOlx;
else if ( match(f(cOlp1?,cOlp2?,cOli1?)) );
	id	f(cOlp1?,cOlp2?,cOli1?) = f(cOlp1,cOlp2,cOli1)*cOldd(cOlp1,cOlp2,1);
	repeat id	cOldd(cOlp1?,cOlp2?,cOlx1?)*cOldd(cOlp1?,cOlp2?,cOlx2?) = cOldd(cOlp1,cOlp2,cOlx1+cOlx2);
	id	cOldd(cOlp1?,cOlp2?,1) = cOldd(cOlp1,cOlp2);
	if ( match(cOldd(cOlp1?,cOlp2?,cOlx?)) );
		id	cOldd(cOlp1?,cOlp2?) = cOldd(cOlp1,cOlp2,1);
		repeat id	cOldd(cOlp1?,cOlp2?,cOlx1?)*cOldd(cOlp3?,cOlp4?,cOlx2?) =
				+theta_(cOlx1-cOlx2)*cOldd(cOlp1,cOlp2,cOlx1)
				+theta_(cOlx2-cOlx1-1)*cOldd(cOlp3,cOlp4,cOlx2);
		id	cOldd(cOlp1?,cOlp2?,cOlx?) = cOldd(cOlp1,cOlp2);
	else;
		repeat;
			id,once,cOldd(cOlp1?,cOlp2?) = cOlddd(cOlp1,cOlp2);
			repeat id	cOlddd(cOlp1?,cOlp2?)*f(cOlp1?,cOli1?,cOli2?) = cOlddd(cOlp1,cOlp2)*cOlf1(cOlp1,cOli1,cOli2);
			id	cOlf1(cOlp1?,cOli1?,cOli2?) = cOlx1*f(cOlp1,cOli1,cOli2);
			repeat id	cOlddd(cOlp1?,cOlp2?)*f(cOlp2?,cOli1?,cOli2?) = cOlddd(cOlp1,cOlp2)*cOlf1(cOlp2,cOli1,cOli2);
			id	cOlf1(cOlp1?,cOli1?,cOli2?) = cOlx2*f(cOlp1,cOli1,cOli2);
			id	cOlddd(cOlp1?,cOlp2?)*cOlx1^cOly1?*cOlx2^cOly2? = cOldd(cOlp1,cOlp2,cOly1,cOly2);
		endrepeat;
		id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?) = theta_(cOlx1-cOlx2)*cOldd(cOlp1,cOlp2,cOlx1,cOlx1+cOlx2)
				+theta_(cOlx2-cOlx1-1)*cOldd(cOlp2,cOlp1,cOlx2,cOlx1+cOlx2);
		repeat;
			id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?)*cOldd(cOlp3?,cOlp4?,cOlx3?,cOlx4?) =
				+theta_(cOlx1-cOlx3-1)*cOldd(cOlp1,cOlp2,cOlx1,cOlx2)
				+theta_(cOlx3-cOlx1-1)*cOldd(cOlp3,cOlp4,cOlx3,cOlx4)
				+delta_(cOlx1-cOlx3)*theta_(cOlx2-cOlx4)*cOldd(cOlp1,cOlp2,cOlx1,cOlx2)
				+delta_(cOlx1-cOlx3)*theta_(cOlx4-cOlx2-1)*cOldd(cOlp3,cOlp4,cOlx3,cOlx4);
		endrepeat;
		id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?) = cOldd(cOlp1,cOlp2);
	endif;
	repeat;
		id	cOldd(cOlp1?,cOlp2?)*cOlp1?.cOlp3? = cOldd(cOlp1,cOlp2)*cOldA1(cOlp3);
		id	cOldd(cOlp1?,cOlp2?)*f(cOlp1?,cOli1?,cOli2?) = cOldd(cOlp1,cOlp2)*cOldA1(cOlk)*f(cOlk,cOli1,cOli2);
		sum cOlk;
	endrepeat;
	repeat id cOldA1(?a)*cOldA1(?b) = cOldA1(?a,?b);
	id	cOldA1(?a) = cOlda1(?a);
	id	cOlda1(cOli1?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?) = 0;
	id	cOlda1(cOli1?,cOli2?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?) =
		-cOlda1(cOli1,cOlp2)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2);
	id	cOlda1(cOli1?,cOli2?,cOli3?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?) =
		-cOlda1(cOli1,cOlp2,cOli3)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOlp2)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2);
	id	cOlda1(cOli1?,cOli2?,cOli3?,cOli4?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?) =
		-cOlda1(cOli1,cOlp2,cOli3,cOli4)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOlp2,cOli4)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOli3,cOlp2)*f(cOli1,cOli4,cOlj1)*cOldd(cOlp1,cOlp2);
	id	cOlda1(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?) =
		-cOlda1(cOli1,cOlp2,cOli3,cOli4,cOli5,cOli6)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOlp2,cOli4,cOli5,cOli6)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOli3,cOlp2,cOli5,cOli6)*f(cOli1,cOli4,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOli3,cOli4,cOlp2,cOli6)*f(cOli1,cOli5,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOli3,cOli4,cOli5,cOlp2)*f(cOli1,cOli6,cOlj1)*cOldd(cOlp1,cOlp2);
	Multiply replace_(cOlda1,cOldA1);
	repeat id cOldA1(cOli1?,cOli2?,?a)*cOldd(cOlp1?,cOlp2?) = cOlp1(cOli1)*cOldA1(cOli2,?a)*cOldd(cOlp1,cOlp2);
	id	cOldA1(cOli1?)*cOldd(cOlp1?,cOlp2?) = cOlp1(cOli1)*cOldd(cOlp1,cOlp2);
	id	cOldd(cOlp1?,cOlp2?) = 1;
endif;
#call adjoint
#call dddff
#call d2f1
#call makeds
TryReplace,cOlpA1,cOlpA2,cOlpA2,cOlpA1;
TryReplace,cOlpA1,cOlpA3,cOlpA3,cOlpA1;
TryReplace,cOlpA1,cOlpA4,cOlpA4,cOlpA1;
TryReplace,cOlpA2,cOlpA3,cOlpA3,cOlpA2;
TryReplace,cOlpA2,cOlpA4,cOlpA4,cOlpA2;
TryReplace,cOlpA3,cOlpA4,cOlpA4,cOlpA3;
Renumber 1;
#call SORT(simpli-`ireduce'-2)
#enddo
if ( match(f(cOlp1?,cOlp2?,cOli1?)*cOlp1?.cOlp2?) );
	repeat id	f(cOlp1?,cOlp2?,cOli1?)*cOlp1?.cOlp2?^cOlx?pos_ = f(cOlp1,cOlp2,cOli1)*cOldd(cOlp2,cOlp1,cOlx);
	id	cOldd(cOlp1?,cOlp2?,1) = cOldd(cOlp1,cOlp2);
	if ( match(cOldd(cOlp1?,cOlp2?,cOlx?)) );
		id	cOldd(cOlp1?,cOlp2?) = cOldd(cOlp1,cOlp2,1);
		repeat id	cOldd(cOlp1?,cOlp2?,cOlx1?)*cOldd(cOlp3?,cOlp4?,cOlx2?) =
			+theta_(cOlx1-cOlx2)*cOldd(cOlp1,cOlp2,cOlx1)*cOlp3.cOlp4^cOlx2
			+theta_(cOlx2-cOlx1-1)*cOldd(cOlp3,cOlp4,cOlx2)*cOlp1.cOlp2^cOlx1;
	else;
		repeat;
			id,once,cOldd(cOlp1?,cOlp2?) = cOlddd(cOlp1,cOlp2);
			repeat id	cOlddd(cOlp1?,cOlp2?)*f(cOlp1?,cOli1?,cOli2?) = cOlddd(cOlp1,cOlp2)*cOlf1(cOlp1,cOli1,cOli2);
			id	cOlf1(cOlp1?,cOli1?,cOli2?) = cOlx1*f(cOlp1,cOli1,cOli2);
			repeat id	cOlddd(cOlp1?,cOlp2?)*f(cOlp2?,cOli1?,cOli2?) = cOlddd(cOlp1,cOlp2)*cOlf1(cOlp2,cOli1,cOli2);
			id	cOlf1(cOlp1?,cOli1?,cOli2?) = cOlx2*f(cOlp1,cOli1,cOli2);
			id	cOlddd(cOlp1?,cOlp2?)*cOlx1^cOly1?*cOlx2^cOly2? = cOldd(cOlp1,cOlp2,cOly1,cOly2);
		endrepeat;
		id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?) = theta_(cOlx1-cOlx2-1)*cOldd(cOlp1,cOlp2,cOlx1,cOlx1+cOlx2)
				+theta_(cOlx2-cOlx1)*cOldd(cOlp2,cOlp1,cOlx2,cOlx1+cOlx2);
		repeat;
			id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?)*cOldd(cOlp3?,cOlp4?,cOlx3?,cOlx4?) =
				+theta_(cOlx1-cOlx3-1)*cOldd(cOlp1,cOlp2,cOlx1,cOlx2)*cOlp3.cOlp4
				+theta_(cOlx3-cOlx1-1)*cOldd(cOlp3,cOlp4,cOlx3,cOlx4)*cOlp1.cOlp2
				+delta_(cOlx1-cOlx3)*theta_(cOlx2-cOlx4-1)*cOldd(cOlp1,cOlp2,cOlx1,cOlx2)*cOlp3.cOlp4
				+delta_(cOlx1-cOlx3)*theta_(cOlx4-cOlx2)*cOldd(cOlp3,cOlp4,cOlx3,cOlx4)*cOlp1.cOlp2;
		endrepeat;
		id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?) = cOldd(cOlp1,cOlp2,1);
	endif;
	repeat;
		id	cOldd(cOlp1?,cOlp2?,cOlx?)*cOlp1?.cOlp3? = cOldd(cOlp1,cOlp2,cOlx)*cOldA1(cOlp3);
		id	cOldd(cOlp1?,cOlp2?,cOlx?)*f(cOlp1?,cOli1?,cOli2?) = cOldd(cOlp1,cOlp2,cOlx)*cOldA1(cOlk)*f(cOlk,cOli1,cOli2);
		sum cOlk;
	endrepeat;
	repeat id cOldA1(?a)*cOldA1(?b) = cOldA1(?a,?b);
	id	cOldA1(?a) = cOlda1(?a);
	id	cOlda1(cOli1?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) = 0;
	id	cOlda1(cOli1?,cOli2?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) =
		-cOlda1(cOli1,cOlp2)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1);
	id	cOlda1(cOli1?,cOli2?,cOli3?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) =
		-cOlda1(cOli1,cOlp2,cOli3)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOlp2)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1);
	id	cOlda1(cOli1?,cOli2?,cOli3?,cOli4?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) =
		-cOlda1(cOli1,cOlp2,cOli3,cOli4)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOlp2,cOli4)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOlp2)*f(cOli1,cOli4,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1);
	id	cOlda1(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) =
		-cOlda1(cOli1,cOlp2,cOli3,cOli4,cOli5)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOlp2,cOli4,cOli5)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOlp2,cOli5)*f(cOli1,cOli4,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOli4,cOlp2)*f(cOli1,cOli5,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1);
	id	cOlda1(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?,cOlx?) =
		-cOlda1(cOli1,cOlp2,cOli3,cOli4,cOli5,cOli6)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOlp2,cOli4,cOli5,cOli6)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOlp2,cOli5,cOli6)*f(cOli1,cOli4,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOli4,cOlp2,cOli6)*f(cOli1,cOli5,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1)
		-cOlda1(cOli1,cOli2,cOli3,cOli4,cOli5,cOlp2)*f(cOli1,cOli6,cOlj1)*cOldd(cOlp1,cOlp2,cOlx)/(cOlx+1);
	Multiply replace_(cOlda1,cOldA1);
	repeat id cOldA1(cOli1?,cOli2?,?a)*cOldd(cOlp1?,cOlp2?,cOlx?) = cOlp1(cOli1)*cOldA1(cOli2,?a)*cOldd(cOlp1,cOlp2,cOlx);
	id	cOldA1(cOli1?)*cOldd(cOlp1?,cOlp2?,cOlx?) = cOlp1(cOli1)*cOldd(cOlp1,cOlp2,cOlx);
	id	cOldd(cOlp1?,cOlp2?,cOlx?) = cOlp1.cOlp2^cOlx;
else if ( match(f(cOlp1?,cOlp2?,cOli1?)) );
	id	f(cOlp1?,cOlp2?,cOli1?) = f(cOlp1,cOlp2,cOli1)*cOldd(cOlp2,cOlp1,1);
	repeat id	cOldd(cOlp1?,cOlp2?,cOlx1?)*cOldd(cOlp1?,cOlp2?,cOlx2?) = cOldd(cOlp1,cOlp2,cOlx1+cOlx2);
	if ( match(cOldd(cOlp1?,cOlp2?,cOlx?)) );
		id	cOldd(cOlp1?,cOlp2?) = cOldd(cOlp1,cOlp2,1);
		repeat id	cOldd(cOlp1?,cOlp2?,cOlx1?)*cOldd(cOlp3?,cOlp4?,cOlx2?) =
				+theta_(cOlx2-cOlx1)*cOldd(cOlp1,cOlp2,cOlx1)
				+theta_(cOlx1-cOlx2-1)*cOldd(cOlp3,cOlp4,cOlx2);
		id	cOldd(cOlp1?,cOlp2?,cOlx?) = cOldd(cOlp1,cOlp2);
	else;
		repeat;
			id,once,cOldd(cOlp1?,cOlp2?) = cOlddd(cOlp1,cOlp2);
			repeat id	cOlddd(cOlp1?,cOlp2?)*f(cOlp1?,cOli1?,cOli2?) = cOlddd(cOlp1,cOlp2)*cOlf1(cOlp1,cOli1,cOli2);
			id	cOlf1(cOlp1?,cOli1?,cOli2?) = cOlx1*f(cOlp1,cOli1,cOli2);
			repeat id	cOlddd(cOlp1?,cOlp2?)*f(cOlp2?,cOli1?,cOli2?) = cOlddd(cOlp1,cOlp2)*cOlf1(cOlp2,cOli1,cOli2);
			id	cOlf1(cOlp1?,cOli1?,cOli2?) = cOlx2*f(cOlp1,cOli1,cOli2);
			id	cOlddd(cOlp1?,cOlp2?)*cOlx1^cOly1?*cOlx2^cOly2? = cOldd(cOlp1,cOlp2,cOly1,cOly2);
		endrepeat;
		id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?) = theta_(cOlx1-cOlx2-1)*cOldd(cOlp1,cOlp2,cOlx1,cOlx1+cOlx2)
				+theta_(cOlx2-cOlx1)*cOldd(cOlp2,cOlp1,cOlx2,cOlx1+cOlx2);
		repeat;
			id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?)*cOldd(cOlp3?,cOlp4?,cOlx3?,cOlx4?) =
				+theta_(cOlx1-cOlx3-1)*cOldd(cOlp1,cOlp2,cOlx1,cOlx2)
				+theta_(cOlx3-cOlx1-1)*cOldd(cOlp3,cOlp4,cOlx3,cOlx4)
				+delta_(cOlx1-cOlx3)*theta_(cOlx2-cOlx4-1)*cOldd(cOlp1,cOlp2,cOlx1,cOlx2)
				+delta_(cOlx1-cOlx3)*theta_(cOlx4-cOlx2)*cOldd(cOlp3,cOlp4,cOlx3,cOlx4);
		endrepeat;
		id	cOldd(cOlp1?,cOlp2?,cOlx1?,cOlx2?) = cOldd(cOlp1,cOlp2);
	endif;
	repeat;
		id	cOldd(cOlp1?,cOlp2?)*cOlp1?.cOlp3? = cOldd(cOlp1,cOlp2)*cOldA1(cOlp3);
		id	cOldd(cOlp1?,cOlp2?)*f(cOlp1?,cOli1?,cOli2?) = cOldd(cOlp1,cOlp2)*cOldA1(cOlk)*f(cOlk,cOli1,cOli2);
		sum cOlk;
	endrepeat;
	repeat id cOldA1(?a)*cOldA1(?b) = cOldA1(?a,?b);
	id	cOldA1(?a) = cOlda1(?a);
	id	cOlda1(cOli1?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?) = 0;
	id	cOlda1(cOli1?,cOli2?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?) =
		-cOlda1(cOli1,cOlp2)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2);
	id	cOlda1(cOli1?,cOli2?,cOli3?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?) =
		-cOlda1(cOli1,cOlp2,cOli3)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOlp2)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2);
	id	cOlda1(cOli1?,cOli2?,cOli3?,cOli4?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?) =
		-cOlda1(cOli1,cOlp2,cOli3,cOli4)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOlp2,cOli4)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOli3,cOlp2)*f(cOli1,cOli4,cOlj1)*cOldd(cOlp1,cOlp2);
	id	cOlda1(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?) =
		-cOlda1(cOli1,cOlp2,cOli3,cOli4,cOli5)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOlp2,cOli4,cOli5)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOli3,cOlp2,cOli5)*f(cOli1,cOli4,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOli3,cOli4,cOlp2)*f(cOli1,cOli5,cOlj1)*cOldd(cOlp1,cOlp2);
	id	cOlda1(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?)*f(cOli1?,cOlp2?,cOlj1?)*cOldd(cOlp1?,cOlp2?) =
		-cOlda1(cOli1,cOlp2,cOli3,cOli4,cOli5,cOli6)*f(cOli1,cOli2,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOlp2,cOli4,cOli5,cOli6)*f(cOli1,cOli3,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOli3,cOlp2,cOli5,cOli6)*f(cOli1,cOli4,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOli3,cOli4,cOlp2,cOli6)*f(cOli1,cOli5,cOlj1)*cOldd(cOlp1,cOlp2)
		-cOlda1(cOli1,cOli2,cOli3,cOli4,cOli5,cOlp2)*f(cOli1,cOli6,cOlj1)*cOldd(cOlp1,cOlp2);
	Multiply replace_(cOlda1,cOldA1);
	repeat id cOldA1(cOli1?,cOli2?,?a)*cOldd(cOlp1?,cOlp2?) = cOlp1(cOli1)*cOldA1(cOli2,?a)*cOldd(cOlp1,cOlp2);
	id	cOldA1(cOli1?)*cOldd(cOlp1?,cOlp2?) = cOlp1(cOli1)*cOldd(cOlp1,cOlp2);
	id	cOldd(cOlp1?,cOlp2?) = 1;
endif;
#call adjoint
#call contract
#call dddff
#call d2f1
#call makeds
TryReplace,cOlpA1,cOlpA2,cOlpA2,cOlpA1;
TryReplace,cOlpA1,cOlpA3,cOlpA3,cOlpA1;
TryReplace,cOlpA1,cOlpA4,cOlpA4,cOlpA1;
TryReplace,cOlpA2,cOlpA3,cOlpA3,cOlpA2;
TryReplace,cOlpA2,cOlpA4,cOlpA4,cOlpA2;
TryReplace,cOlpA3,cOlpA4,cOlpA4,cOlpA3;
*TryReplace,cOlpR1,cOlpR2,cOlpR2,cOlpR1;
*TryReplace,cOlpR1,cOlpR3,cOlpR3,cOlpR1;
*TryReplace,cOlpR1,cOlpR4,cOlpR4,cOlpR1;
*TryReplace,cOlpR2,cOlpR3,cOlpR3,cOlpR2;
*TryReplace,cOlpR2,cOlpR4,cOlpR4,cOlpR2;
*TryReplace,cOlpR3,cOlpR4,cOlpR4,cOlpR3;
Renumber 1;
if ( count(cOlpR1,1,cOlpR2,1,cOlpA1,1,cOlpA2,1) == 16 );
id	f(cOlpR1,cOlpA1,cOli1?)*f(cOlpR2,cOlpA2,cOli1?)*cOlpR1.cOlpR2*cOlpR1.cOlpA2*cOlpR2.cOlpA1*cOlpA1.cOlpA2^2 =
		-f(cOlpR1,cOli1,cOlpR2)*f(cOlpR2,cOli1,cOlpR1)*cOlpR1.cOlpR2*cA^4/72
		+f(cOlpA2,cOli1,cOlpA1)*f(cOli1,cOlpA2,cOlpA1)*cOlpA1.cOlpA2^2*d33(cOlpR1,cOlpR2)/2/NA;
id	f(cOlpR2,cOlpA1,cOli1?)*f(cOlpA1,cOlpA2,cOli1?)*cOlpR1.cOlpR2*cOlpR1.cOlpA1*cOlpR1.cOlpA2*cOlpR2.cOlpA2*cOlpA1.cOlpA2 =
	+cA^2/12*f(cOlpR2,cOlpA2,cOlpR1)*f(cOlpR1,cOlpA2,cOlpR2)*cOlpR1.cOlpA2*cOlpR2.cOlpA2
	-1/4/NA*d33(cOlpR1,cOlpR2)*f(cOlpA1,cOli1,cOlpA2)*f(cOli1,cOlpA1,cOlpA2)*cOlpA1.cOlpA2^2
	-cOlpR1.cOlpR2*cOlpR1.cOlpA1*cOlpR1.cOlpA2*cOlpR2.cOlpA1*cOlpR2.cOlpA2*cOlpA1.cOlpA2^2*cA/4;
endif;
#define redolo "0"
if ( count(f,1) > 0 );
	redefine redolo "1";
endif;
#call SORT(simpli-`ireduce'-3)
#if `redolo' == 0
#define ireduce "1000"
#endif
#enddo
#endif
#endprocedure
*
*--#] simpli : 
*--#[ dddff :
*
#procedure dddff
*
*	Takes our one irreducible object (14 vertices) and puts it in cOldddff.
*	This puts it out of range of the other operations.
*	We apply a reduction identity when there are at least two dA in it.
*	It is symmetric in its arguments.
*
*	Made by J.Vermaseren, 24-may-1997
*
if ( count(f,1) == 2 );
	if ( count(<cOlpR1,1>,...,<cOlpR`RANK',1>,<cOlpA1,1>,...,<cOlpA`RANK',1>) == 12 );
		#do ir1 = 1,`RANK'-1
		#do ir2 = `ir1'+1,`RANK'
			if ( ( match(f(cOlpR`ir1',cOli1?,cOli2?)) == 2 )
			&& ( match(f(cOlpR`ir2',cOli1?,cOli2?)) == 2 )
			&& ( count(cOlpR`ir1',1,cOlpR`ir2',1) == 8 ) );
				id	f(cOlpR`ir1',cOlpR`ir2',cOli1?)*f(cOlpR`ir1',cOlpR`ir2',cOli1?)*
						cOlpR`ir1'.cOlp?^2*cOlpR`ir2'.cOlp?^2 =
						cOldRdR(cOlpR`ir1',cOlpR`ir2',cOlp);
			elseif ( ( match(f(cOlpA`ir1',cOli1?,cOli2?)) == 2 )
			&& ( match(f(cOlpA`ir2',cOli1?,cOli2?)) == 2 )
			&& ( count(cOlpA`ir1',1,cOlpA`ir2',1) == 8 ) );
				id	f(cOlpA`ir1',cOlpA`ir2',cOli1?)*f(cOlpA`ir1',cOlpA`ir2',cOli1?)*
						cOlpA`ir1'.cOlp?^2*cOlpA`ir2'.cOlp?^2 =
						cOldRdR(cOlpA`ir1',cOlpA`ir2',cOlp);
			endif;
		#enddo
		#enddo
		#do ir1 = 1,`RANK'
		#do ir2 = 1,`RANK'
			if ( ( match(f(cOlpR`ir1',cOli1?,cOli2?)) == 2 )
			&& ( match(f(cOlpA`ir2',cOli1?,cOli2?)) == 2 )
			&& ( count(cOlpR`ir1',1,cOlpA`ir2',1) == 8 ) );
				id	f(cOlpR`ir1',cOlpA`ir2',cOli1?)*f(cOlpR`ir1',cOlpA`ir2',cOli1?)*
						cOlpR`ir1'.cOlp?^2*cOlpA`ir2'.cOlp?^2 =
						cOldRdR(cOlpR`ir1',cOlpA`ir2',cOlp);
			endif;
		#enddo
		#enddo
		#do ir = 1,`RANK'
		if ( match(cOldRdR(cOlp1?,cOlp2?,cOlpR`ir')) );
			if ( count(cOlpR`ir',1) > 1 );
				id	cOldRdR(cOlp1?,cOlp2?,cOlpR`ir') = f(cOlp1,cOlp2,cOlk)*f(cOlp1,cOlp2,cOlk)*
								cOlp1.cOlpR`ir'^2*cOlp2.cOlpR`ir'^2;
			else;
				id	cOldRdR(cOlp1?,cOlp2?,cOlpR`ir') = cOldddff(cOlp1,cOlp2,cOlpR`ir');
			endif;
		endif;
		if ( match(cOldRdR(cOlp1?,cOlp2?,cOlpA`ir')) );
			if ( count(cOlpA`ir',1) > 1 );
				id	cOldRdR(cOlp1?,cOlp2?,cOlpA`ir') = f(cOlp1,cOlp2,cOlk)*f(cOlp1,cOlp2,cOlk)*
								cOlp1.cOlpA`ir'^2*cOlp2.cOlpA`ir'^2;
			else;
				id	cOldRdR(cOlp1?,cOlp2?,cOlpA`ir') = cOldddff(cOlp1,cOlp2,cOlpA`ir');
			endif;
		endif;
		#enddo
	elseif ( count(<cOlpR1,1>,...,<cOlpR`RANK',1>,<cOlpA1,1>,...,<cOlpA`RANK',1>) == 14 );
		id f(cOlpR1,cOlpA1,cOli1?)*f(cOlpR2,cOlpA1,cOli1?)*cOlpR1.cOlpR2^3*cOlpR1.cOlpA1*cOlpR2.cOlpA1 =
				cOldff554(cOlpR1,cOlpR2,cOlpA1);
	endif;
endif;
symmetrize cOldddff;
 
id	cOldddff(cOlp1?cOlpAs,cOlp2?cOlpAs,cOlp3?cOlpAs) =
			-2/27*cA^3*d44(cOlp1,cOlp2)+19/15*cA*d444(cOlp1,cOlp2,cOlp3)-8/9*d644(cOlp1,cOlp2,cOlp3);
id	cOldddff(cOlp1?,cOlp2?cOlpAs,cOlp3?cOlpAs) =
			-2/27*cA^3*d44(cOlp1,cOlp2)+19/15*cA*d444(cOlp1,cOlp2,cOlp3)-8/9*d644(cOlp2,cOlp1,cOlp3);

#endprocedure
*
*--#] dddff : 
*--#[ d2f1 :
*
#procedure d2f1
*
*	Routine implements two relations.
*	1: Triangles of two cOldR and one f for which one of the cOldR has only
*	   one external leg.
*	2: Pairs of cOldR with each one external leg.
*	With the new version of simpli.prc this routine is still used, but
*	in principle simpli could have done without. It does make convergence
*	a little bit faster.
*
*	Completed 24-may-1997, J.Vermaseren
*
#do ir1 = 1,`RANK'-1
  if ( match(f(cOlpR`ir1',cOli1?,cOli2?)) );
#do ir2 = `ir1'+1,`RANK'
	if ( count(cOlpR`ir1',1) && count(cOlpR`ir2',1) );
		id	cOlpR`ir1' = cOlx1*cOlpR`ir1';
		id	cOlpR`ir2' = cOlx2*cOlpR`ir2';
		id	f(cOlpR`ir1',cOlpR`ir2',cOli1?) = f(cOlpR`ir1',cOlpR`ir2',cOli1)*cOlx3/cOlx1/cOlx2;
		id	cOlpR`ir1'.cOlpR`ir2' = cOlpR`ir1'.cOlpR`ir2'/cOlx1/cOlx2;
		if ( count(cOlx3,1) == 1 );
			if ( count(cOlx1,1) == 1 );
				id	f(cOlpR`ir1',cOlpR`ir2',cOli1?)*cOlpR`ir1'.cOlpR`ir2'^cOlx? = cOlorig(cOlx,cOli1);
				id	cOlpR`ir1' = cOldR`ir1'(?);
				id	cOlorig(cOlx?,cOli1?)*cOldR`ir1'(cOli2?) = -1/(cOlx+1)*
						f(cOlpR`ir1',cOli2,cOli1)*cOlpR`ir1'.cOlpR`ir2'^cOlx*cOlpR`ir1'.cOlpR`ir2';
			elseif ( count(cOlx2,1) == 1 );
				id	f(cOlpR`ir2',cOlpR`ir1',cOli1?)*cOlpR`ir1'.cOlpR`ir2'^cOlx? = cOlorig(cOlx,cOli1);
				id	cOlpR`ir2' = cOldR`ir2'(?);
				id	cOlorig(cOlx?,cOli1?)*cOldR`ir2'(cOli2?) = -1/(cOlx+1)*
						f(cOlpR`ir2',cOli2,cOli1)*cOlpR`ir1'.cOlpR`ir2'^cOlx*cOlpR`ir1'.cOlpR`ir2';
			endif;
		endif;
		id	cOlx3 = 1;
	endif;
	id	cOlx1 = 1;
	id	cOlx2 = 1;
#enddo
  endif;
#enddo
#do ir1 = 1,`RANK'-1
  if ( match(f(cOlpA`ir1',cOli1?,cOli2?)) );
#do ir2 = `ir1'+1,`RANK'
	if ( count(cOlpA`ir1',1) && count(cOlpA`ir2',1) );
		id	cOlpA`ir1' = cOlx1*cOlpA`ir1';
		id	cOlpA`ir2' = cOlx2*cOlpA`ir2';
		id	f(cOlpA`ir1',cOlpA`ir2',cOli1?) = f(cOlpA`ir1',cOlpA`ir2',cOli1)*cOlx3/cOlx1/cOlx2;
		id	cOlpA`ir1'.cOlpA`ir2' = cOlpA`ir1'.cOlpA`ir2'/cOlx1/cOlx2;
		if ( count(cOlx3,1) == 1 );
			if ( count(cOlx1,1) == 1 );
				id	f(cOlpA`ir1',cOlpA`ir2',cOli1?)*cOlpA`ir1'.cOlpA`ir2'^cOlx? = cOlorig(cOlx,cOli1);
				id	cOlpA`ir1' = cOldA`ir1'(?);
				id	cOlorig(cOlx?,cOli1?)*cOldA`ir1'(cOli2?) = -1/(cOlx+1)*
						f(cOlpA`ir1',cOli2,cOli1)*cOlpA`ir1'.cOlpA`ir2'^cOlx*cOlpA`ir1'.cOlpA`ir2';
			elseif ( count(cOlx2,1) == 1 );
				id	f(cOlpA`ir2',cOlpA`ir1',cOli1?)*cOlpA`ir1'.cOlpA`ir2'^cOlx? = cOlorig(cOlx,cOli1);
				id	cOlpA`ir2' = cOldA`ir2'(?);
				id	cOlorig(cOlx?,cOli1?)*cOldA`ir2'(cOli2?) = -1/(cOlx+1)*
						f(cOlpA`ir2',cOli2,cOli1)*cOlpA`ir1'.cOlpA`ir2'^cOlx*cOlpA`ir1'.cOlpA`ir2';
			endif;
		endif;
		id	cOlx3 = 1;
	endif;
	id	cOlx1 = 1;
	id	cOlx2 = 1;
#enddo
  endif;
#enddo
#do ir1 = 1,`RANK'
  if ( match(f(cOlpR`ir1',cOli1?,cOli2?)) );
#do ir2 = 1,`RANK'
	if ( count(cOlpR`ir1',1) && count(cOlpA`ir2',1) );
		id	cOlpR`ir1' = cOlx1*cOlpR`ir1';
		id	cOlpA`ir2' = cOlx2*cOlpA`ir2';
		id	f(cOlpR`ir1',cOlpA`ir2',cOli1?) = f(cOlpR`ir1',cOlpA`ir2',cOli1)*cOlx3/cOlx1/cOlx2;
		id	cOlpR`ir1'.cOlpA`ir2' = cOlpR`ir1'.cOlpA`ir2'/cOlx1/cOlx2;
		if ( count(cOlx3,1) == 1 );
			if ( count(cOlx1,1) == 1 );
				id	f(cOlpR`ir1',cOlpA`ir2',cOli1?)*cOlpR`ir1'.cOlpA`ir2'^cOlx? = cOlorig(cOlx,cOli1);
				id	cOlpR`ir1' = cOldR`ir1'(?);
				id	cOlorig(cOlx?,cOli1?)*cOldR`ir1'(cOli2?) = -1/(cOlx+1)*
						f(cOlpR`ir1',cOli2,cOli1)*cOlpR`ir1'.cOlpA`ir2'^cOlx*cOlpR`ir1'.cOlpA`ir2';
			elseif ( count(cOlx2,1) == 1 );
				id	f(cOlpA`ir2',cOlpR`ir1',cOli1?)*cOlpR`ir1'.cOlpA`ir2'^cOlx? = cOlorig(cOlx,cOli1);
				id	cOlpA`ir2' = cOldA`ir2'(?);
				id	cOlorig(cOlx?,cOli1?)*cOldA`ir2'(cOli2?) = -1/(cOlx+1)*
						f(cOlpA`ir2',cOli2,cOli1)*cOlpR`ir1'.cOlpA`ir2'^cOlx*cOlpR`ir1'.cOlpA`ir2';
			endif;
		endif;
		id	cOlx3 = 1;
	endif;
	id	cOlx1 = 1;
	id	cOlx2 = 1;
#enddo
  endif;
#enddo

Multiply cOly;
while ( count(cOly,1) );
  id cOly = 1;
  #do ir1 = 1,`RANK'-1
  #do ir2 = `ir1'+1,`RANK'
	if ( count(cOlpR`ir1',1) && count(cOlpR`ir2',1) );
		id	cOlpR`ir1'.cOlpR`ir2'^cOlx? = cOlorig(cOlx);
		if ( ( count(cOlpR`ir1',1) == 1 ) && ( count(cOlpR`ir2',1) == 1 ) );
			id	cOlpR`ir1' = cOldR`ir1'(?);
			id	cOlpR`ir2' = cOldR`ir2'(?);
			id	cOlorig(cOlx?)*cOldR`ir1'(cOli1?)*cOldR`ir2'(cOli2?) =
						cOly*d_(cOli1,cOli2)/NA*cOlpR`ir1'.cOlpR`ir2'^cOlx*cOlpR`ir1'.cOlpR`ir2';
		else;	
			id	cOlorig(cOlx?) = cOlpR`ir1'.cOlpR`ir2'^cOlx;
		endif;
	endif;
  #enddo
  #enddo

  #do ir1 = 1,`RANK'-1
  #do ir2 = `ir1'+1,`RANK'
	if ( count(cOlpA`ir1',1) && count(cOlpA`ir2',1) );
		id	cOlpA`ir1'.cOlpA`ir2'^cOlx? = cOlorig(cOlx);
		if ( ( count(cOlpA`ir1',1) == 1 ) && ( count(cOlpA`ir2',1) == 1 ) );
			id	cOlpA`ir1' = cOldA`ir1'(?);
			id	cOlpA`ir2' = cOldA`ir2'(?);
			id	cOlorig(cOlx?)*cOldA`ir1'(cOli1?)*cOldA`ir2'(cOli2?) =
						cOly*d_(cOli1,cOli2)/NA*cOlpA`ir1'.cOlpA`ir2'^cOlx*cOlpA`ir1'.cOlpA`ir2';
		else;	
			id	cOlorig(cOlx?) = cOlpA`ir1'.cOlpA`ir2'^cOlx;
		endif;
	endif;
  #enddo
  #enddo

  #do ir1 = 1,`RANK'
  #do ir2 = 1,`RANK'
	if ( count(cOlpR`ir1',1) && count(cOlpA`ir2',1) );
		id	cOlpR`ir1'.cOlpA`ir2'^cOlx? = cOlorig(cOlx);
		if ( ( count(cOlpR`ir1',1) == 1 ) && ( count(cOlpA`ir2',1) == 1 ) );
			id	cOlpR`ir1' = cOldR`ir1'(?);
			id	cOlpA`ir2' = cOldA`ir2'(?);
			id	cOlorig(cOlx?)*cOldR`ir1'(cOli1?)*cOldA`ir2'(cOli2?) =
						cOly*d_(cOli1,cOli2)/NA*cOlpR`ir1'.cOlpA`ir2'^cOlx*cOlpR`ir1'.cOlpA`ir2';
		else;	
			id	cOlorig(cOlx?) = cOlpR`ir1'.cOlpA`ir2'^cOlx;
		endif;
	endif;
  #enddo
  #enddo
endwhile;
*
#endprocedure
*
*--#] d2f1 : 
*--#[ makeds :
*
#procedure makeds
*
*	Tries to rewrite completed results in terms of d functions.
*	This is not as easy as one might think because there are many
*	potential topologies and we would like to use a minimum number
*	of statements. It has become much simpler after symmetric functions
*	started to work.
*	Routine completed 24-may-1997 by J.Vermaseren
*
#do isim1 = 1,`RANK'
#do isim2 = 1,`RANK'
	if ( ( count(cOlpR`isim1',1) == 3 ) && ( count(cOlpA`isim2',1) == 4 )
		&& ( match(cOlpR`isim1'.cOlpA`isim2') == 2 ) )
		id	cOlpR`isim1'.cOlpA`isim2'^2 = cA^2/6*replace_(cOlpA`isim2',cOlpR`isim1');
	if ( ( count(cOlpR`isim1',1) == 3 ) && ( count(cOlpR`isim2',1) == 4 )
		&& ( match(cOlpR`isim1'.cOlpR`isim2') == 3 ) ) discard;
	if ( ( count(cOlpR`isim1',1) == 4 ) && ( count(cOlpR`isim2',1) == 5 )
		&& ( match(cOlpR`isim1'.cOlpR`isim2') == 4 ) ) discard;
	if ( ( count(cOlpR`isim1',1) == 3 ) && ( count(cOlpA`isim2',1) == 4 )
		&& ( match(cOlpR`isim1'.cOlpR`isim2') == 3 ) ) discard;
	if ( ( count(cOlpA`isim1',1) == 4 ) && ( count(cOlpR`isim2',1) == 5 )
		&& ( match(cOlpR`isim1'.cOlpR`isim2') == 4 ) ) discard;
#enddo
#enddo

if ( ( count(f,1) == 0 )
		&& ( count(<cOlpR1,1,cOlpA1,1>,...,<cOlpR`RANK',1,cOlpA`RANK',1>) ) );
  #do ir = 1,`RANK'
    id cOlpR`ir' = cOlx*cOlpR`ir';
    id cOlpA`ir' = cOlx*cOlpA`ir';
  #enddo
  #do ir = 1,`RANK'
    totensor,cOlpR`ir',cOldr`ir';
  #enddo
  #do ir = 1,`RANK'
    totensor,cOlpA`ir',cOlda`ir';
  #enddo
  renumber;
  repeat;
	id cOldr1?cOldar[cOlx3](cOli1?,cOli2?,cOli3?)*cOldr2?cOldar[cOlx4](cOli1?,cOli2?,cOli4?) =
			d33(cOlpAR[cOlx3],cOlpAR[cOlx4])*cOlx1*d_(cOli3,cOli4)/NA;
	id cOldr1?cOldar[cOlx3](cOli1?,...,cOli4?)*cOldr2?cOldar[cOlx4](cOli1?,...,cOli3?,cOli5?) =
			d44(cOlpAR[cOlx3],cOlpAR[cOlx4])*cOlx1*d_(cOli4,cOli5)/NA;
	id cOldr1?cOldar[cOlx3](cOli1?,...,cOli5?)*cOldr2?cOldar[cOlx4](cOli1?,...,cOli4?,cOli6?) =
			d55(cOlpAR[cOlx3],cOlpAR[cOlx4])*cOlx1*d_(cOli5,cOli6)/NA;
  endrepeat;
  if ( count(cOlx1,1) );
    id cOlx = 1;
    id cOlx1 = 1;
    #do ir = 1,`RANK'
      tovector,cOlpR`ir',cOldr`ir';
    #enddo
    #do ir = 1,`RANK'
      tovector,cOlpA`ir',cOlda`ir';
    #enddo
    #do ir = 1,`RANK'
      id cOlpR`ir' = cOlx*cOlpR`ir';
      id cOlpA`ir' = cOlx*cOlpA`ir';
    #enddo
    #do ir = 1,`RANK'
      totensor,cOlpR`ir',cOldr`ir';
    #enddo
    #do ir = 1,`RANK'
      totensor,cOlpA`ir',cOlda`ir';
    #enddo
    renumber;
  endif;
  id cOldr1?cOldar(cOli1?,cOli2?,cOli3?)*cOlda1?cOldar(cOli1?,cOli2?,cOli3?,cOli4?) = 0;
  id cOldr1?cOldar(cOli1?,cOli2?,cOli3?,cOli4?)*cOlda1?cOldar(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?) = 0;
  if ( count(cOlx,1) == 6 );
	id cOldr1?cOldar[cOlx3](cOli1?,...,cOli3?)*cOldr2?cOldar[cOlx4](cOli1?,...,cOli3?) = d33(cOlpAR[cOlx3],cOlpAR[cOlx4]);
    symmetrize d33;
  elseif ( count(cOlx,1) == 8 );
	id cOldr1?cOldar[cOlx3](cOli1?,...,cOli4?)*cOldr2?cOldar[cOlx4](cOli1?,...,cOli4?) = d44(cOlpAR[cOlx3],cOlpAR[cOlx4]);
    symmetrize d44;
  elseif ( count(cOlx,1) == 10 );
	id cOldr1?cOldar[cOlx3](cOli1?,...,cOli5?)*cOldr2?cOldar[cOlx4](cOli1?,...,cOli5?) = d55(cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli4?)*cOldr1?cOldar[cOlx3](cOli1?,cOli2?,cOli5?)*cOldr2?cOldar[cOlx4](cOli3?,...,cOli5?) = d433(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
    symmetrize d55;
    symmetrize d433,2,3;
  elseif ( count(cOlx,1) == 12 );
	id cOldr1?cOldar[cOlx3](cOli1?,...,cOli6?)*cOldr2?cOldar[cOlx4](cOli1?,...,cOli6?) = d66(cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli4?)*cOldr1?cOldar[cOlx3](cOli1?,cOli2?,cOli5?,cOli6?)*cOldr2?cOldar[cOlx4](cOli3?,...,cOli6?)
				 = d444(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli6?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli3?)*cOldr2?cOldar[cOlx4](cOli4?,...,cOli6?) = d633(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOldr1?cOldar[cOlx3](cOli1?,cOli2?,cOli3?)*cOldr2?cOldar[cOlx4](cOli1?,cOli4?,cOli5?)*cOlda1?cOldar[cOlx1](cOli2?,cOli4?,cOli6?)
			*cOlda2?cOldar[cOlx2](cOli3?,cOli5?,cOli6?) = d3333(cOlpAR[cOlx3],cOlpAR[cOlx4],cOlpAR[cOlx1],cOlpAR[cOlx2]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli5?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli3?,cOli6?)*cOldr2?cOldar[cOlx4](cOli4?,...,cOli6?) = d543(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id,many,cOldr1?cOldar[cOlx3](cOli1?,...,cOli3?)*cOldr2?cOldar[cOlx4](cOli1?,...,cOli4?) =
			d33(cOlpAR[cOlx3],cOlpAR[cOlx4])*d_(cOli3,cOli4)/NA;
    symmetrize d33;
    symmetrize d66;
    symmetrize d444;
    symmetrize d633,2,3;
  elseif ( count(cOlx,1) == 14 );
	id cOldr1?cOldar[cOlx3](cOli1?,...,cOli7?)*cOldr2?cOldar[cOlx4](cOli1?,...,cOli7?) = d77(cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOldr1?cOldar[cOlx3](cOli1?,cOli2?,cOli3?)*cOldr2?cOldar[cOlx4](cOli1?,cOli2?,cOli4?) =
			d33(cOlpAR[cOlx3],cOlpAR[cOlx4])*d_(cOli3,cOli4)/NA;
	id cOldr1?cOldar[cOlx3](cOli1?,...,cOli4?)*cOldr2?cOldar[cOlx4](cOli1?,...,cOli3?,cOli5?) =
			d44(cOlpAR[cOlx3],cOlpAR[cOlx4])*d_(cOli4,cOli5)/NA;
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli7?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli4?)*cOldr2?cOldar[cOlx4](cOli5?,...,cOli7?)
				 = d743(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli6?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli3?,cOli7?)*cOldr2?cOldar[cOlx4](cOli4?,...,cOli7?)
				 = d644(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli5?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli3?,cOli6?,cOli7?)*cOldr2?cOldar[cOlx4](cOli4?,...,cOli7?)
				 = d554(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli6?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli4?,cOli7?)*cOldr2?cOldar[cOlx4](cOli5?,...,cOli7?)
				 = d653(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli5?)*cOldr1?cOldar[cOlx3](cOli1?,cOli2?,cOli6?)*cOldr2?cOldar[cOlx4](cOli3?,cOli4?,cOli7?)
			*cOlda2?cOldar[cOlx2](cOli6?,cOli6?,cOli7?) = d5333(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4],cOlpAR[cOlx2]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli4?)*cOlda2?cOldar[cOlx2](cOli1?,cOli5?,...,cOli7?)*cOldr1?cOldar[cOlx3](cOli2?,cOli3?,cOli5?)
			*cOldr2?cOldar[cOlx4](cOli4?,cOli6?,cOli7?) = d4433a(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli4?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli5?,cOli6?)*cOldr1?cOldar[cOlx3](cOli3?,cOli5?,cOli7?)
			*cOldr2?cOldar[cOlx4](cOli4?,cOli6?,cOli7?) = d4433b(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli4?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli5?,cOli6?)*cOldr1?cOldar[cOlx3](cOli3?,cOli4?,cOli7?)
			*cOldr2?cOldar[cOlx4](cOli5?,cOli6?,cOli7?) = d4433c(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
    symmetrize d33;
    symmetrize d44;
    symmetrize d77;
    symmetrize d644,2,3;
    symmetrize d554,1,2;
	symmetrize d5333,2,3;
  elseif ( count(cOlx,1) == 16 );
*
*   There are actually 23 topologies that need to be defined here.
*	We have here at least the set needed for the adjoint (5 topologies).
*	At least 5 of the 23 can be reduced later.
*
	id cOldr1?cOldar[cOlx3](cOli1?,...,cOli8?)*cOldr2?cOldar[cOlx4](cOli1?,...,cOli8?) = d88(cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli8?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli4?)*cOldr2?cOldar[cOlx4](cOli5?,...,cOli8?)
				 = d844(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli8?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli5?)*cOldr2?cOldar[cOlx4](cOli6?,...,cOli8?)
				 = d853(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli7?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli5?,cOli8?)*cOldr2?cOldar[cOlx4](cOli6?,...,cOli8?)
				 = d763(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli7?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli4?,cOli8?)*cOldr2?cOldar[cOlx4](cOli5?,...,cOli8?)
				 = d754(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli7?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli3?)*cOldr1?cOldar[cOlx3](cOli4?,cOli5?,cOli8?)
			*cOldr2?cOldar[cOlx4](cOli6?,cOli7?,cOli8?) = d7333(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli6?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli4?,cOli7?,cOli8?)*cOldr2?cOldar[cOlx4](cOli5?,...,cOli8?)
				 = d664(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli6?)*cOldr1?cOldar[cOlx3](cOli1?,...,cOli3?,cOli7?,cOli8?)*cOldr2?cOldar[cOlx4](cOli4?,...,cOli8?)
				 = d655(cOlpAR[cOlx1],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli6?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli7?,cOli8?)
		*cOldr1?cOldar[cOlx3](cOli3?,cOli4?,cOli5?)*cOldr2?cOldar[cOlx4](cOli6?,cOli7?,cOli8?)
				 = d6433a(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli6?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli7?,cOli8?)
		*cOldr1?cOldar[cOlx3](cOli3?,cOli4?,cOli7?)*cOldr2?cOldar[cOlx4](cOli5?,cOli6?,cOli8?)
				 = d6433b(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli6?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli3?,cOli7?)
		*cOldr1?cOldar[cOlx3](cOli4?,cOli5?,cOli8?)*cOldr2?cOldar[cOlx4](cOli6?,cOli7?,cOli8?)
				 = d6433c(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli5?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli6?,cOli7?,cOli8?)
		*cOldr1?cOldar[cOlx3](cOli3?,cOli4?,cOli6?)*cOldr2?cOldar[cOlx4](cOli5?,cOli6?,cOli8?)
				 = d5533a(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli5?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli6?,cOli7?,cOli8?)
		*cOldr1?cOldar[cOlx3](cOli3?,cOli4?,cOli5?)*cOldr2?cOldar[cOlx4](cOli6?,cOli7?,cOli8?)
				 = d5533b(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli5?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli3?,cOli6?,cOli7?)
		*cOldr1?cOldar[cOlx3](cOli4?,cOli6?,cOli8?)*cOldr2?cOldar[cOlx4](cOli5?,cOli7?,cOli8?)
				 = d5533c(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli5?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli3?,cOli6?,cOli7?)
		*cOldr1?cOldar[cOlx3](cOli4?,cOli5?,cOli8?)*cOldr2?cOldar[cOlx4](cOli6?,cOli7?,cOli8?)
				 = d5533d(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli5?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli6?,cOli7?)
		*cOldr1?cOldar[cOlx3](cOli3?,cOli6?,cOli7?,cOli8?)*cOldr2?cOldar[cOlx4](cOli4?,cOli5?,cOli8?)
				 = d5443a(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli5?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli3?,cOli6?)
		*cOldr1?cOldar[cOlx3](cOli4?,cOli6?,cOli7?,cOli8?)*cOldr2?cOldar[cOlx4](cOli5?,cOli7?,cOli8?)
				 = d5443b(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli5?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli6?,cOli7?)
		*cOldr1?cOldar[cOlx3](cOli3?,cOli4?,cOli6?,cOli8?)*cOldr2?cOldar[cOlx4](cOli5?,cOli7?,cOli8?)
				 = d5443c(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli5?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli3?,cOli6?)
		*cOldr1?cOldar[cOlx3](cOli4?,cOli5?,cOli7?,cOli8?)*cOldr2?cOldar[cOlx4](cOli6?,cOli7?,cOli8?)
				 = d5443d(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli4?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli5?,cOli6?)*cOldr1?cOldar[cOlx3](cOli5?,...,cOli8?)
			*cOldr2?cOldar[cOlx4](cOli3?,cOli4?,cOli7?,cOli8?) = d4444a(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli4?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli5?,cOli6?)*cOldr1?cOldar[cOlx3](cOli3?,cOli5?,cOli7?,cOli8?)
			*cOldr2?cOldar[cOlx4](cOli4?,cOli6?,cOli7?,cOli8?) = d4444b(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli4?)*cOlda2?cOldar[cOlx2](cOli1?,cOli5?,cOli6?)
			*cOldr1?cOldar[cOlx3](cOli2?,cOli5?,cOli7?)*cOldr2?cOldar[cOlx4](cOli3?,cOli6?,cOli8?)
			*cOldr3?cOldar[cOlx5](cOli4?,cOli7?,cOli8?) = d43333a(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4],cOlpAR[cOlx5]);
	id cOlda1?cOldar[cOlx1](cOli1?,...,cOli4?)*cOlda2?cOldar[cOlx2](cOli1?,cOli2?,cOli5?)
			*cOldr1?cOldar[cOlx3](cOli3?,cOli6?,cOli7?)*cOldr2?cOldar[cOlx4](cOli4?,cOli6?,cOli8?)
			*cOldr3?cOldar[cOlx5](cOli5?,cOli7?,cOli8?) = d43333b(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4],cOlpAR[cOlx5]);
    symmetrize d33;
    symmetrize d44;
    symmetrize d55;
    symmetrize d88;
    symmetrize d844,2,3;
    symmetrize d664,1,2;
    rcyclesymmetrize d4444a;
	symmetrize d4444b,1,2;
	symmetrize d4444b,3,4;
  else;
*   We don't know yet what to do.
  endif;
  id cOlx^cOly? = 1;
*
*   Some dependencies
*
  id d5443b(cOlp1?,cOlp2?,cOlp3?cOlpAs,cOlp4?) = d543(cOlp1,cOlp2,cOlp4);
  id d5443d(cOlp1?,cOlp2?,cOlp3?cOlpAs,cOlp4?) = d543(cOlp1,cOlp2,cOlp4);
  id d6433a(cOlp1?,cOlp2?cOlpAs,cOlp3?,cOlp4?) = d633(cOlp1,cOlp3,cOlp4);
  id d43333b(cOlp1?cOlpAs,cOlp2?,cOlp3?,cOlp4?,cOlp5?) = cA^2/6*d3333(cOlp2,cOlp3,cOlp4,cOlp5);
  id d6433a(cOlp1?cOlpRs,cOlp2?,cOlp3?,cOlp4?) = -1/8*cA*d4433c(cOlp1,cOlp2,cOlp3,cOlp4)
		-1/4*cA*d4433a(cOlp1,cOlp2,cOlp3,cOlp4)-1/4*I2R*cA^2*d433(cOlp2,cOlp3,cOlp4)
		+1/NR*d33(cOlp1,cOlp3)*d433(cOlp2,cOlp1,cOlp4);
  id d6433a(cOlp1?cOlpAs,cOlp2?,cOlp3?,cOlp4?) = -1/8*cA*d4433c(cOlp1,cOlp2,cOlp3,cOlp4)
		-1/4*cA*d4433a(cOlp1,cOlp2,cOlp3,cOlp4)-1/4*cA^3*d433(cOlp2,cOlp3,cOlp4);
  id d5533b(cOlp1?,cOlp2?,cOlp3?,cOlp4?) = d33(cOlp1,cOlp3)*d33(cOlp2,cOlp4)/NA*(cR-cA/4)^2;
  id d633(cOlp1?cOlpRs,cOlp2?,cOlp3?) = -3/8*cA*d433(cOlp1,cOlp2,cOlp3)
			-1/40*I2R*cA^2*d33(cOlp2,cOlp3)+d33(cOlp1,cOlp2)*d33(cOlpR4,cOlp3)/NR;
  id d633(cOlp1?cOlpAs,cOlp2?,cOlp3?) = -3/8*cA*d433(cOlp1,cOlp2,cOlp3)-1/40*cA^3*d33(cOlp2,cOlp3);
  id d743(cOlp1?cOlpRs,cOlp2?,cOlp3?) = -1/2*cA*d543(cOlp1,cOlp2,cOlp3)
		+1/NR*d33(cOlpR4,cOlp3)*d44(cOlp1,cOlp2)-43/120/NA*d33(cOlp1,cOlp3)*d44(cOlpA4,cOlp2)
		-23/1440*cA^2*d433(cOlp2,cOlp1,cOlp3)+49/60*d4433b(cOlpA4,cOlp2,cOlp1,cOlp3);
  id d4433a(cOlp1?cOlpAs,cOlp2?,cOlp3?,cOlp4?) = 1/6*cA^2*d433(cOlp2,cOlp3,cOlp4);
  id d4433a(cOlp1?,cOlp2?cOlpAs,cOlp3?,cOlp4?) = 1/6*cA^2*d433(cOlp1,cOlp3,cOlp4);
  id d4433c(cOlp1?cOlpAs,cOlp2?,cOlp3?,cOlp4?) = 1/6*cA^2*d433(cOlp2,cOlp3,cOlp4);
  id d4433c(cOlp1?,cOlp2?cOlpAs,cOlp3?,cOlp4?) = 1/6*cA^2*d433(cOlp1,cOlp3,cOlp4);
  id d433(cOlp1?cOlpAs,cOlp2?,cOlp3?) = 1/6*cA^2*d33(cOlp2,cOlp3);
  id d66(cOlpA1,cOlpA2) = 5/8*d444(cOlpA1,cOlpA2,cOlpA3)-7/240*cA^2*d44(cOlpA1,cOlpA2)
			-1/864*cA^6*NA;
  id d4433b(cOlpA1,cOlpA2,cOlpR2,cOlpR1) = d4433b(cOlpA1,cOlpA2,cOlpR1,cOlpR2);
  id d4433b(cOlpA2,cOlpA1,cOlpR2,cOlpR1) = d4433b(cOlpA1,cOlpA2,cOlpR1,cOlpR2);
  #do ir = 1,`RANK'
    tovector,cOlpR`ir',cOldr`ir';
  #enddo
  #do ir = 1,`RANK'
    tovector,cOlpA`ir',cOlda`ir';
  #enddo
else if ( ( count(f,1) == 2 ) && (
	count(<cOlpR1,1>,...,<cOlpR`RANK',1>,<cOlpA1,1>,...,<cOlpA`RANK',1>) == 14 ) );
*
*	We have here a few terms that manage to construct a holding pattern.
*
  #do ir = 1,`RANK'
    totensor,cOlpR`ir',cOldr`ir';
  #enddo
  #do ir = 1,`RANK'
    totensor,cOlpA`ir',cOlda`ir';
  #enddo
  renumber;
  id cOlda1?cOldar[cOlx1](cOli1?,...,cOli4?)*cOlda2?cOldar[cOlx2](cOli3?,cOli5?,cOli6?,cOli7?)*
	cOldr1?cOldar[cOlx3](cOli4?,cOli6?,cOli8?)*cOldr2?cOldar[cOlx4](cOli7?,cOli8?,cOli9?)*f(cOli1?,cOli5?,cOli10?)*f(cOli2?,cOli9?,cOli10?) =
			+cA/4*d4433b(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx3],cOlpAR[cOlx4])
		+cOlda1(cOli1,cOli2,cOli3,cOli5)*cOlda2(cOli3,cOli5,cOli6,cOli7)*cOldr1(cOli4,cOli1,cOli8)*cOldr2(cOli7,cOli8,cOli9)
			*f(cOli6,cOli4,cOli10)*f(cOli2,cOli9,cOli10);
  id cOlda1?cOldar[cOlx1](cOli1?,...,cOli4?)*cOlda2?cOldar[cOlx2](cOli2?,cOli3?,cOli5?,cOli6?)*
	cOldr1?cOldar[cOlx3](cOli6?,cOli7?,cOli8?)*cOldr2?cOldar[cOlx4](cOli4?,cOli7?,cOli9?)*f(cOli1?,cOli8?,cOli10?)*f(cOli5?,cOli9?,cOli10?) =
			+cA/4*d4433c(cOlpAR[cOlx1],cOlpAR[cOlx2],cOlpAR[cOlx4],cOlpAR[cOlx3])
			-cA/6/NA*d33(cOlpAR[cOlx3],cOlpAR[cOlx4])*d44(cOlpAR[cOlx1],cOlpAR[cOlx2]);
  id d4433c(cOlp1?cOlpAs,cOlp2?,cOlp3?,cOlp4?) = 1/6*cA^2*d433(cOlp2,cOlp3,cOlp4);
  id d4433c(cOlp1?,cOlp2?cOlpAs,cOlp3?,cOlp4?) = 1/6*cA^2*d433(cOlp1,cOlp3,cOlp4);
  id d433(cOlp1?cOlpAs,cOlp2?,cOlp3?) = 1/6*cA^2*d33(cOlp2,cOlp3);
  #do ir = 1,`RANK'
    tovector,cOlpR`ir',cOldr`ir';
  #enddo
  #do ir = 1,`RANK'
    tovector,cOlpA`ir',cOlda`ir';
  #enddo
  Symmetrize,d33;
  Symmetrize,d44;
  Symmetrize d4444b,1,2;
  Symmetrize d4444b,3,4;
  id d4433b(cOlpA1,cOlpA2,cOlpR2,cOlpR1) = d4433b(cOlpA1,cOlpA2,cOlpR1,cOlpR2);
  id d4433b(cOlpA2,cOlpA1,cOlpR2,cOlpR1) = d4433b(cOlpA1,cOlpA2,cOlpR1,cOlpR2);
else if ( ( count(f,1) == 2 ) && (
	count(<cOlpR1,1>,...,<cOlpR`RANK',1>,<cOlpA1,1>,...,<cOlpA`RANK',1>) == 12 ) );
*
*	We have here a few terms that manage to construct a holding pattern.
*
  #do ir = 1,`RANK'
    totensor,cOlpR`ir',cOldr`ir';
  #enddo
  renumber;
  id cOlda1?cOldar[cOlx1](cOli1?,cOli2?,cOli3?)*cOlda2?cOldar[cOlx2](cOli1?,cOli4?,cOli5?)*f(cOli3?,cOli8?,cOli9?)*
	cOldr1?cOldar[cOlx3](cOli2?,cOli6?,cOli7?)*cOldr2?cOldar[cOlx4](cOli5?,cOli7?,cOli8?)*f(cOli4?,cOli9?,cOli6?) =
		+cA/NA/4*d33(cOlpAR[cOlx1],cOlpAR[cOlx2])*d33(cOlpAR[cOlx3],cOlpAR[cOlx4])
		-cA/NA/4*d33(cOlpAR[cOlx1],cOlpAR[cOlx3])*d33(cOlpAR[cOlx2],cOlpAR[cOlx4])
			;
  #do ir = 1,`RANK'
    tovector,cOlpR`ir',cOldr`ir';
  #enddo
  Symmetrize,d3333;
  Symmetrize d33;
endif;
*
#endprocedure
*
*--#] makeds : 
*--#[ contract :
*
#procedure contract
*
*	Remove contracted indices in the same invariant.
*	These objects are not supposed to occur very often.
*
*	Routine by J.Vermaseren, 24-may-1997
*
repeat;
#do isim = 1,`RANK'
if ( match(cOlpR`isim'.cOlpR`isim') );
	ToTensor cOlpR`isim',cOldR1;
	id	cOldR1(?a,cOli1?,?b,cOli1?,?c) = cOldR1(cOli1,cOli1,?a,?b,?c);
	id	cOldR1(cOli1?,cOli1?) = NA*I2R;
	id	cOldR1(cOli5?,cOli5?,cOli1?) = 0;
	id	cOldR1(cOli5?,cOli5?,cOli1?,cOli2?) = (cR-cA/6)*d_(cOli1,cOli2)*I2R;
	id	cOldR1(cOli5?,cOli5?,cOli1?,cOli2?,cOli3?) =
			(cR-cA/4)*cOlpR`isim'(cOli1)*cOlpR`isim'(cOli2)*cOlpR`isim'(cOli3);
	id	cOldR1(cOli5?,cOli5?,cOli1?,cOli2?,cOli3?,cOli4?) =
			cOlpR`isim'(cOli1)*cOlpR`isim'(cOli2)*cOlpR`isim'(cOli3)*cOlpR`isim'(cOli4)*(cR-cA/3)
			+cOldA(cOli1,cOli2,cOli3,cOli4)*I2R/30;
	id	cOldR1(cOli6?,cOli6?,cOli1?,cOli2?,cOli3?,cOli4?,cOli5?) =
			cOlpR`isim'(cOli1)*cOlpR`isim'(cOli2)*cOlpR`isim'(cOli3)*cOlpR`isim'(cOli4)*cOlpR`isim'(cOli5)
				*(cR-5*cA/12)+(
			+cOlpR`isim'(cOli1)*cOlpR`isim'(cOli2)*cOldA(cOlpR`isim',cOli3,cOli4,cOli5)
			+cOlpR`isim'(cOli1)*cOlpR`isim'(cOli3)*cOldA(cOlpR`isim',cOli2,cOli4,cOli5)
			+cOlpR`isim'(cOli1)*cOlpR`isim'(cOli4)*cOldA(cOlpR`isim',cOli2,cOli3,cOli5)
			+cOlpR`isim'(cOli1)*cOlpR`isim'(cOli5)*cOldA(cOlpR`isim',cOli2,cOli3,cOli4)
			+cOlpR`isim'(cOli2)*cOlpR`isim'(cOli3)*cOldA(cOlpR`isim',cOli1,cOli4,cOli5)
			+cOlpR`isim'(cOli2)*cOlpR`isim'(cOli4)*cOldA(cOlpR`isim',cOli1,cOli3,cOli5)
			+cOlpR`isim'(cOli2)*cOlpR`isim'(cOli5)*cOldA(cOlpR`isim',cOli1,cOli3,cOli4)
			+cOlpR`isim'(cOli3)*cOlpR`isim'(cOli4)*cOldA(cOlpR`isim',cOli1,cOli2,cOli5)
			+cOlpR`isim'(cOli3)*cOlpR`isim'(cOli5)*cOldA(cOlpR`isim',cOli1,cOli2,cOli4)
			+cOlpR`isim'(cOli4)*cOlpR`isim'(cOli5)*cOldA(cOlpR`isim',cOli1,cOli2,cOli3)
			)/10*I2R/12;
	id	cOldR1(cOli7?,cOli7?,cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?) =
			cOlpR`isim'(cOli1)*cOlpR`isim'(cOli2)*cOlpR`isim'(cOli3)*cOlpR`isim'(cOli4)*cOlpR`isim'(cOli5)
				*cOlpR`isim'(cOli6)*(cR-cA/2)
			+1/6*cOldA(cOlpR`isim',cOlpR`isim',cOlpR`isim',cOlpR`isim')*
				dd_(cOli1,cOli2,cOli3,cOli4,cOli5,cOli6)/15/NA^3
			-1/42*I2R*cOldA(cOli1,cOli2,cOli3,cOli4,cOli5,cOli6);
	if ( count(cOldA,1) == 0 );
#do isimpli = 1,`RANK'
	elseif ( count(cOlpA`isimpli',1) == 0 );
		id,once,cOldA(?a) = cOldA`isimpli'(?a);
		ToVector,cOldA`isimpli',cOlpA`isimpli';
#enddo
	endif;
endif;
#enddo
#do isim = 1,`RANK'
if ( match(cOlpA`isim'.cOlpA`isim') );
	ToTensor cOlpA`isim',cOldA1;
	id	cOldA1(?a,cOli1?,?b,cOli1?,?c) = cOldA1(cOli1,cOli1,?a,?b,?c);
	id	cOldA1(cOli1?,cOli1?) = NA*cA;
	id	cOldA1(cOli5?,cOli5?,cOli1?,cOli2?) = 5/6*cA^2*d_(cOli1,cOli2);
	id	cOldA1(cOli5?,cOli5?,cOli1?,cOli2?,cOli3?,cOli4?) =
			+7/10*cA*cOlpA`isim'(cOli1)*cOlpA`isim'(cOli2)*cOlpA`isim'(cOli3)*cOlpA`isim'(cOli4);
	id	cOldA1(cOli7?,cOli7?,cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?) =
			+10/21*cA*cOldA(cOli1,cOli2,cOli3,cOli4,cOli5,cOli6)
			+1/6*cOldA(cOlpA`isim',cOlpA`isim',cOlpA`isim',cOlpA`isim')*
				dd_(cOli1,cOli2,cOli3,cOli4,cOli5,cOli6)/15/NA^3;
	if ( count(cOldA,1) == 0 );
#do isimpli = 1,`RANK'
	elseif ( count(cOlpA`isimpli',1) == 0 );
		id,once,cOldA(?a) = cOldA`isimpli'(?a);
		ToVector,cOldA`isimpli',cOlpA`isimpli';
#enddo
	endif;
endif;
#enddo
repeat;
id cOlda1?cOldas(cOli1?,cOli2?,cOli3?,cOli3?) = 5/6*cA^2*d_(cOli1,cOli2);
id cOlda1?cOldas(cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli5?) = 7/10*cA*cOlda1(cOli1,cOli2,cOli3,cOli4);
id cOlda1?cOldas[cOlx1](cOli1?,cOli2?,cOli3?,cOli4?,cOli5?,cOli6?,cOli7?,cOli7?) =
			+10/21*cA*cOlda1(cOli1,cOli2,cOli3,cOli4,cOli5,cOli6)
			+1/6*d44(cOlpAs[cOlx1],cOlpA4)*dd_(cOli1,cOli2,cOli3,cOli4,cOli5,cOli6)/15/NA^3;
endrepeat;

#do isim1 = 1,`RANK'
#do isim2 = 1,`RANK'
	if ( ( count(cOlpR`isim1',1) == 3 ) && ( count(cOlpA`isim2',1) == 4 )
		&& ( match(cOlpR`isim1'.cOlpA`isim2') == 2 ) )
		id	cOlpR`isim1'.cOlpA`isim2'^2 = cA^2/6*replace_(cOlpA`isim2',cOlpR`isim1');
	if ( ( count(cOlpR`isim1',1) == 3 ) && ( count(cOlpR`isim2',1) == 4 )
		&& ( match(cOlpR`isim1'.cOlpR`isim2') == 3 ) ) discard;
	if ( ( count(cOlpR`isim1',1) == 4 ) && ( count(cOlpR`isim2',1) == 5 )
		&& ( match(cOlpR`isim1'.cOlpR`isim2') == 4 ) ) discard;
	if ( ( count(cOlpR`isim1',1) == 3 ) && ( count(cOlpA`isim2',1) == 4 )
		&& ( match(cOlpR`isim1'.cOlpR`isim2') == 3 ) ) discard;
	if ( ( count(cOlpA`isim1',1) == 4 ) && ( count(cOlpR`isim2',1) == 5 )
		&& ( match(cOlpR`isim1'.cOlpR`isim2') == 4 ) ) discard;
#enddo
#enddo
EndRepeat;
Renumber;
#endprocedure
*
*--#] contract : 
*--#[ docolor :
*
#procedure docolor
#call color
#call SORT(docolor-1)
#call adjoint
#call SORT(docolor-2)
#call simpli
id	cOlacc(cOlx?) = cOlx;
#endprocedure
*
*--#] docolor : 
"""


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    logging.basicConfig(
        format = '[%(asctime)s %(levelname)5s] %(message)s',
        datefmt = "%H:%M:%S",
        level = logging.INFO,
    )
    main(args)
