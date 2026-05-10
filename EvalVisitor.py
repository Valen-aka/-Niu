
from antlr4 import *
import operator

oper = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '**': operator.pow
}

rel = {
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '>': operator.gt,
    '<=': operator.le,
    '>=': operator.ge
}

if __name__ is not None and "." in __name__:
    from .ñuParser import ñuParser
    from .ñuVisitor import ñuVisitor
else:
    from ñuParser import ñuParser
    from ñuVisitor import ñuVisitor

class EvalVisitor(ñuVisitor):
    def __init__(self):
        self.memory = {}

    def inferir_tipo(self, valor):
        if isinstance(valor, bool):
            return "bool"
        elif isinstance(valor, (int, float)):
            return "num"
        elif isinstance(valor, str):
            return "texto"
        else:
            raise Exception("Tipo no soportado")

    def validar_tipo(self, tipo, valor):
        if tipo == "num":
            return isinstance(valor, (int, float))
        elif tipo == "texto":
            return isinstance(valor, str)
        elif tipo == "bool":
            return isinstance(valor, bool)
        return False

    def visitRoot(self, ctx):
        l = list(ctx.getChildren())
        for i in range(len(l) - 1):  # ignorar EOF
            result = self.visit(l[i])
        return result

    def visitAddSub(self, ctx):
        l = list(ctx.getChildren())
        return oper[l[1].getText()](
            self.visit(l[0]),
            self.visit(l[2])
        )

    def visitMulDiv(self, ctx):
        l = list(ctx.getChildren())
        return oper[l[1].getText()](
            self.visit(l[0]),
            self.visit(l[2])
        )

    def visitPotencia(self, ctx):
        l = list(ctx.getChildren())
        return oper[l[1].getText()](
            self.visit(l[0]),
            self.visit(l[2])
        )

    def visitComparador(self, ctx):
        l = list(ctx.getChildren())
        if len(l) == 1:  # expresión normal
            return self.visit(l[0])
        return int(
            rel[l[1].getText()](
                self.visit(l[0]),
                self.visit(l[2])
            )
        )

    def visitDeclaracion(self, ctx):
        l = list(ctx.getChildren())
        tipo = l[0].getText()
        nombre = l[1].getText()
        valor = self.visit(l[3])

        if tipo == 'auto':
            tipo = self.inferir_tipo(valor)

        if not self.validar_tipo(tipo, valor):
            raise Exception(f"Tipo incompatible para '{nombre}'")

        self.memory[nombre] = {
            'tipo': tipo,
            'valor': valor
        }
        return valor

    def visitAsignacion(self, ctx):
        l = list(ctx.getChildren())
        nombre = l[0].getText()
        valor = self.visit(l[2])

        if nombre not in self.memory:
            raise Exception(f"Variable '{nombre}' no definida")

        tipo = self.memory[nombre]['tipo']
        if not self.validar_tipo(tipo, valor):
            raise Exception(f"Tipo incompatible para '{nombre}'")

        self.memory[nombre]['valor'] = valor
        return valor

    def visitVariable(self, ctx):
        nombre = ctx.getText()
        if nombre in self.memory:
            return self.memory[nombre]['valor']
        raise Exception(f"Variable '{nombre}' no definida")

    def visitNumero(self, ctx):
        texto = ctx.getText()
        return float(texto) if '.' in texto else int(texto)

    def visitTexto(self, ctx):
        texto = ctx.getText()
        return texto[1:-1]

    def visitBooleano(self, ctx):
        return True if ctx.getText() == 'verdadero' else False

    def visitCondition(self, ctx):
        l = list(ctx.getChildren())
        # Si principal (if)
        if self.visit(l[1]) == 1:  # l[1] es la expresión del "si" (x > 5)
            return self.visit(l[2])  # l[2] es el bloque asociado al "si"

        # osino (elif)
        index = 3
        while index < len(l):
            texto = l[index].getText()
            if texto == 'osino':
                condicion = l[index + 1]
                bloque = l[index + 2]
                if self.visit(condicion) == 1:
                    return self.visit(bloque)
                index += 3
            elif texto == 'sino':
                return self.visit(l[index + 1])
            else:
                index += 1

    def visitBloque(self, ctx):
        l = list(ctx.getChildren())
        for child in l:
            if child.getText() not in ['{', '}']:
                result = self.visit(child)
        return result

    def visitPrint(self, ctx):
        print(self.visit(ctx.mostrarStat().expr()))

    def visitIngresarExpr(self, ctx):
        texto = input()
        try:
            return float(texto) if '.' in texto else int(texto)
        except:
            return texto