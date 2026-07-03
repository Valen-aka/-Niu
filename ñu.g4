grammar ñu;

root: stat+ EOF;

declaracion
    : tipo ID ASIG expr
    ;

asignacion
    : ID ASIG expr
    ;

stat
    : declaracion       # ToDeclaracion
    | asignacion        # ToAsignacion
    | mostrarStat       # Print
    | ifStat            # ToIf
    | whileStat         # ToWhile
    | forStat           # ToFor
    | funcionStat       # ToFuncion
    | returnStat        # ToReturn
    | expr              # ExprStat
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

whileStat: MIENTRAS expr bloque
        # While
       ;

forInit
    : declaracion       # InitDeclaracion
    | asignacion        # InitAsignacion
    ;

forUpdate
    : asignacion        # UpdateAsignacion
    ;

forStat
    : PARA LPAREN
      forInit
      PYC
      expr
      PYC
      forUpdate
      RPAREN
      bloque
      # For
    ;

funcionStat
    : FUNCION
      ID
      LPAREN
      parametros?
      RPAREN
      bloque
      # Funcion
    ;

parametros
    : parametro (COMA parametro)*
    ;

parametro
    : tipo ID
    ;

llamadaFuncion
    : ID LPAREN argumentos? RPAREN 
    ;

argumentos
    : expr (COMA expr)*
    ;

returnStat
    : RETORNAR expr?
      # Return
    ;

bloque: LKEY stat* RKEY;

addExpr: addExpr op=(MAS | MENOS) mulExpr # AddSub
        | mulExpr                         # ToMul
        ;

mulExpr: mulExpr op=(MULT | DIV) powExpr  # MulDiv
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
    | ingresarExpr           # Input
    | llamadaFuncion         # AtomFuncion
    | ID                     # Variable
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

MIENTRAS: 'mientras';
PARA : 'para';
PYC : ';';

FUNCION: 'funcion';
COMA: ',';
RETORNAR : 'retornar';

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