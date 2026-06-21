grammar ñu;

root: stat+ EOF;

stat: tipo ID ASIG expr      # Declaracion
    | ID ASIG expr           # Asignacion
    | mostrarStat            # Print
    | ifStat                 # ToIf
    | expr                   # ExprStat
    ;

mostrarStat: MOSTRAR LPAREN expr RPAREN;

tipo: NUM_TIPO | TEXTO_TIPO | BOOL_TIPO | AUTO;

expr: compExpr;

compExpr: addExpr (op=(IGUAL | DIF | MENOR_IGUAL | MAYOR_IGUAL | MENOR | MAYOR) addExpr)? # Comparador
        ;

ifStat : SI expr bloque
        (ELIF expr bloque)*
        (SINO bloque)?
        # Condition
       ;

bloque: LKEY stat* RKEY;

addExpr: addExpr op=(MAS | MENOS) mulExpr # AddSub
        | mulExpr                         # ToMul
        ;

mulExpr: mulExpr MULT powExpr  # Multiplicacion
        | mulExpr DIV powExpr  # Division
        | powExpr              # ToPow
        ;

powExpr: <assoc=right> atom ELEVADO powExpr  # Potencia
      | atom                   # ToAtom
      ;

atom
    : LPAREN expr RPAREN     # Parentesis
    | NUM                    # Numero
    | STRING                 # Texto
    | BOOL                   # Booleano
    | ID                     # Variable
    | ingresarExpr           # Input
    | MENOS atom             # Negativo
    ;

ingresarExpr: INGRESAR LPAREN RPAREN;


// === Signos y palabras reservadas ===
SI: 'si';
SINO: 'sino';
ELIF: 'osino';

LKEY: '{';
RKEY: '}';

IGUAL: '==';
DIF: '!=';
MENOR_IGUAL: '<=';
MAYOR_IGUAL: '>=';
MENOR: '<';
MAYOR: '>';

MOSTRAR: 'mostrar';
INGRESAR: 'ingresar';

NUM_TIPO: 'num';
TEXTO_TIPO: 'texto';
BOOL_TIPO: 'bool';
AUTO: 'auto';

BOOL: 'verdadero' | 'falso';
STRING: '"' .*? '"' | '\'' .*? '\'';
NUM : [0-9]+ ('.' [0-9]+)? ;

ID  : [a-zA-ZáéíóúÁÉÍÓÚñÑ_][a-zA-ZáéíóúÁÉÍÓÚñÑ_0-9]* ;

ASIG: '=';

LPAREN: '(';
RPAREN: ')';
MULT: '*';
DIV: '/';
MAS : '+' ;
MENOS : '-' ;
ELEVADO: '**';


WS : [ \t\r\n]+ -> skip ;
