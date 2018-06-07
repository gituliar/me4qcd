#include me4qcd.h # Declarations

#define DEBUG

#procedure read(x) 
Skip;
#if `x' == 0
  NSkip AMP;
  #include `AMP' # Declarations
  L AMP =
  #do i = 1,$n
    + amp(`i')*(
    #include `AMP' # d`i'
    )
  #enddo
  ;
#else
  #include `AMPx' # Declarations
  NSkip AMPx;
  L AMPx =
  #do i = 1,$n
    + ampx(`i')*(
    #include `AMPx' # d`i'
    )
    #do j=1,9
        * replace_(l`j', r`j')
    #enddo
  #enddo
  ;
#endif

#ifdef `SET'
id amp(n1?!{,`SET'}) = 0;
#endif

#ifdef `SETx'
id ampx(n1?!{,`SETx'}) = 0;
#endif

#do V={VQQA, VQQG, VGGG} 
id `V'(n1?pos_,k1?, n2?,k2?, n3?,k3?) = `V'(i(n1),k1, n2,k2, n3,k3);
id `V'(n1?,k1?, n2?pos_,k2?, n3?,k3?) = `V'(n1,k1, i(n2),k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, n3?pos_,k3?) = `V'(n1,k1, n2,k2, i(n3),k3);
id `V'(n1?neg_,k1?, n2?,k2?, n3?,k3?) = `V'(e(-n1),k1, n2,k2, n3,k3);
id `V'(n1?,k1?, n2?neg_,k2?, n3?,k3?) = `V'(n1,k1, e(-n2),k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, n3?neg_,k3?) = `V'(n1,k1, n2,k2, e(-n3),k3);
#enddo
id VGGGG(n1?neg_,k1?, n2?,k2?, n3?,k3?, n4?,k4?) = VGGGG(e(-n1),k1, n2,k2, n3,k3, n4,k4);
id VGGGG(n1?,k1?, n2?neg_,k2?, n3?,k3?, n4?,k4?) = VGGGG(n1,k1, e(-n2),k2, n3,k3, n4,k4);
id VGGGG(n1?,k1?, n2?,k2?, n3?neg_,k3?, n4?,k4?) = VGGGG(n1,k1, n2,k2, e(-n3),k3, n4,k4);
id VGGGG(n1?,k1?, n2?,k2?, n3?,k3?, n4?neg_,k4?) = VGGGG(n1,k1, n2,k2, n3,k3, e(-n4),k4);
id VGGGG(n1?pos_,k1?, n2?,k2?, n3?,k3?, n4?,k4?) = VGGGG(i(n1),k1, n2,k2, n3,k3, n4,k4);
id VGGGG(n1?,k1?, n2?pos_,k2?, n3?,k3?, n4?,k4?) = VGGGG(n1,k1, i(n2),k2, n3,k3, n4,k4);
id VGGGG(n1?,k1?, n2?,k2?, n3?pos_,k3?, n4?,k4?) = VGGGG(n1,k1, n2,k2, i(n3),k3, n4,k4);
id VGGGG(n1?,k1?, n2?,k2?, n3?,k3?, n4?pos_,k4?) = VGGGG(n1,k1, n2,k2, n3,k3, i(n4),k4);

* In QGRAF rays with two consequtive indices are connected by a propagator,
* (1,2), (3,4), etc. Let us make this connection explicit, so that all
* internal indices are odd. We assume
*   * n1,n2,n3 are positive for internal lines
#do V={VQQA, VQQG, VGGG} 
id `V'(i(n1?even_),k1?, n2?,k2?, n3?,k3?) = `V'(i(n1-1),k1, n2,k2, n3,k3);
id `V'(n1?,k1?, i(n2?even_),k2?, n3?,k3?) = `V'(n1,k1, i(n2-1),k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, i(n3?even_),k3?) = `V'(n1,k1, n2,k2, i(n3-1),k3);
#enddo
id VGGGG(i(n1?even_),k1?, n2?,k2?, n3?,k3?, n4?,k4?) = VGGGG(i(n1-1),k1, n2,k2, n3,k3, n4,k4);
id VGGGG(n1?,k1?, i(n2?even_),k2?, n3?,k3?, n4?,k4?) = VGGGG(n1,k1, i(n2-1),k2, n3,k3, n4,k4);
id VGGGG(n1?,k1?, n2?,k2?, i(n3?even_),k3?, n4?,k4?) = VGGGG(n1,k1, n2,k2, i(n3-1),k3, n4,k4);
id VGGGG(n1?,k1?, n2?,k2?, n3?,k3?, i(n4?even_),k4?) = VGGGG(n1,k1, n2,k2, n3,k3, i(n4-1),k4);
* In QGRAF all momenta go into the vertex. Let us change fermions'momentum
* to flow along the particle-number flow.
#do V={VQQA, VQQG} 
id `V'(n1?,k1?, i(n2?),k2?, n3?,k3?) = `V'(n1,k1, i(n2),-k2, n3,k3);
#enddo
* Invert momentum for final-state particles so that it is outgoing now.
#do V={VQQA,VQQG,VGGG} 
id `V'(e(n1?even_),k1?, n2?,k2?, n3?,k3?) = `V'(e(n1),-k1, n2,k2, n3,k3);
id `V'(n1?,k1?, e(n2?even_),k2?, n3?,k3?) = `V'(n1,k1, e(n2),-k2, n3,k3);
id `V'(n1?,k1?, n2?,k2?, e(n3?even_),k3?) = `V'(n1,k1, n2,k2, e(n3),-k3);
#enddo
id VGGGG(e(n1?even_),k1?, n2?,k2?, n3?,k3?, n4?,k4?) = VGGGG(e(n1),-k1, n2,k2, n3,k3, n4,k4);
id VGGGG(n1?,k1?, e(n2?even_),k2?, n3?,k3?, n4?,k4?) = VGGGG(n1,k1, e(n2),-k2, n3,k3, n4,k4);
id VGGGG(n1?,k1?, n2?,k2?, e(n3?even_),k3?, n4?,k4?) = VGGGG(n1,k1, n2,k2, e(n3),-k3, n4,k4);
id VGGGG(n1?,k1?, n2?,k2?, n3?,k3?, e(n4?even_),k4?) = VGGGG(n1,k1, n2,k2, n3,k3, e(n4),-k4);

* Conjugated amplitude?
#if `x' == 1
* Change indexes of internal lines to be all even
  #do V={VQQA,VQQG,VGGG} 
  id `V'(i(n1?),k1?, n2?,k2?, n3?,k3?) = `V'(i(n1+1),k1, n2,k2, n3,k3);
  id `V'(n1?,k1?, i(n2?),k2?, n3?,k3?) = `V'(n1,k1, i(n2+1),k2, n3,k3);
  id `V'(n1?,k1?, n2?,k2?, i(n3?),k3?) = `V'(n1,k1, n2,k2, i(n3+1),k3);
  #enddo
  id VGGGG(i(n1?),k1?, n2?,k2?, n3?,k3?, n4?,k4?) = VGGGG(i(n1+1),k1, n2,k2, n3,k3, n4,k4);
  id VGGGG(n1?,k1?, i(n2?),k2?, n3?,k3?, n4?,k4?) = VGGGG(n1,k1, i(n2+1),k2, n3,k3, n4,k4);
  id VGGGG(n1?,k1?, n2?,k2?, i(n3?),k3?, n4?,k4?) = VGGGG(n1,k1, n2,k2, i(n3+1),k3, n4,k4);
  id VGGGG(n1?,k1?, n2?,k2?, n3?,k3?, i(n4?),k4?) = VGGGG(n1,k1, n2,k2, n3,k3, i(n4+1),k4);
* Invert momentum flow for fermions.
  #do V={VQQA, VQQG} 
  id `V'(n1?,k1?, n2?,k2?, n3?,k3?) = `V'(n2,k2, n1,k1, n3,-k3);
  #enddo
#endif

#ifdef `DEBUG'
  Print +ss;
#endif
.sort
#endprocedure


#call read(0)
#call read(1)

L ME2 = AMP*AMPx;
*id amp(ex1?)*ampx(ex2?) = amp(ex1,ex2);
id amp(ex1?)*ampx(ex2?) = 1;
.sort
Drop AMP,AMPx;

#include me4qcd.h # ColorTrace
#include me4qcd.h # ExpandFeynmanRules

#include me4qcd.h # GammaTrace
#include me4qcd.h # Clean

id m = 4-2*ep;
id q.q = 1;
id p1.p1 = 0;
id p2.p2 = 0;
id k1.k1 = 0;
id k2.k2 = 0;
id k3.k3 = 0;
id k4.k4 = 0;
id k5.k5 = 0;
id k6.k6 = 0;
id p1?.p2? = sp(p1,p2);

id Ca = 3;
id Cf = 4/3;
id Tf = 1/2;
id Na = 8;
.sort

Bracket den;
.sort
Collect num;
.sort

#ifdef `DEBUG'
  Print +ss;
#endif
Format Mathematica;
#write <`ME2'> "(%E)", ME2

.end
