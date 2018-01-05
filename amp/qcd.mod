
#   PROPAGATORS
#
    [a, a, +, external;  color_id='cj', field_id='Photon',
                         index_id='v',
                         prop_id='A',
                         anti_in_id=(''),
                         anti_out_id=('')]

    [q,  Q, -, notadpole; color_id='ci',
                          field_id='Quark',
                          index_id='s',
                          prop_id='Q',
                          anti_in_id=('U','Vx'),
                          anti_out_id=('Ux','V')]

    [g,  g,  +, notadpole; color_id='cj', field_id='Gluon',
                           index_id='v',
                           prop_id='G',
                           anti_in_id=(''),
                           anti_out_id=('')]

#
#   color_id represents color indices and is
#      * ci<n> in fundamental (NF-dimensional) representation
#      * cj<n> in adjoint (NA-dimensional) representation
#   field_id is
#      * a for photon
#      * g for gluon
#      * q for quark
#      * Q for anti-quark
#   index_id is
#      * v<n> for vector indices
#      * s<n> for spinor indices
   

#   VERTICES
#
    [q, Q, a;     vertex_id='VQQA']

    [q, Q, g;     vertex_id='VQQG']

    [g, g, g;      vertex_id='VGGG']

    [g, g, g, g;  vertex_id='VGGGG']
#
#     vertex_id is a name of a vertex function in FORM
