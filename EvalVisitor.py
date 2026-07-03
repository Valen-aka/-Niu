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
        self.functions = {}

    # === Helpers ===
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

    # === Roots y bloque ===
    def visitRoot(self, ctx):
        l = list(ctx.getChildren())
        for i in range(len(l) - 1):
            result = self.visit(l[i])
        return result

    def visitBloque(self, ctx):
        l = list(ctx.getChildren())
        for child in l:
            if child.getText() not in ['{', '}']:
                result = self.visit(child)
        return result

    # === Variables ===
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

    def visitToDeclaracion(self, ctx):
        return self.visit(ctx.declaracion())

    def visitInitDeclaracion(self, ctx):
        return self.visit(ctx.declaracion())

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

    def visitToAsignacion(self, ctx):
        return self.visit(ctx.asignacion())

    def visitInitAsignacion(self, ctx):
        return self.visit(ctx.asignacion())

    def visitUpdateAsignacion(self, ctx):
        return self.visit(ctx.asignacion())

    def visitVariable(self, ctx):
        nombre = ctx.getText()
        if nombre in self.memory:
            return self.memory[nombre]['valor']
        raise Exception(f"Variable '{nombre}' no definida")

    # === Valores ===
    def visitNumero(self, ctx):
        texto = ctx.getText()
        return float(texto) if '.' in texto else int(texto)

    def visitTexto(self, ctx):
        texto = ctx.getText()
        return texto[1:-1]

    def visitBooleano(self, ctx):
        return True if ctx.getText() == 'verdadero' else False

    # === Expresiones matematicas y comparaciones ===
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
        if len(l) == 1:
            return self.visit(l[0])
        return int(
            rel[l[1].getText()](
                self.visit(l[0]),
                self.visit(l[2])
            )
        )

    def visitParentesis(self, ctx):
        return self.visit(ctx.expr())

    def visitNegativo(self, ctx):
        return -self.visit(ctx.atom())

    # === Condicionales y bucles ===
    def visitCondition(self, ctx):
        l = list(ctx.getChildren())
        if self.visit(l[1]) == 1:
            return self.visit(l[2])
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

    def visitWhile(self, ctx):
        l = list(ctx.getChildren())
        condicion = l[1]
        bloque = l[2]
        while self.visit(condicion):
            self.visit(bloque)

    def visitFor(self, ctx):
        self.visit(ctx.forInit())
        while self.visit(ctx.expr()):
            self.visit(ctx.bloque())
            self.visit(ctx.forUpdate())

    # === Input / Output ===
    def visitPrint(self, ctx):
        print(self.visit(ctx.mostrarStat().expr()))

    def visitIngresarExpr(self, ctx):
        texto = input()
        try:
            return float(texto) if '.' in texto else int(texto)
        except:
            return texto
    
    # === Funciones ===
    def visitToFuncion(self, ctx):
        return self.visit(ctx.funcionStat())
        
    def visitFuncion(self, ctx):
        nombre = ctx.ID().getText()
        parametros = []

        if ctx.parametros():
            for p in ctx.parametros().parametro():
                tipo = p.tipo().getText()
                nombre_param = p.ID().getText()

                parametros.append(
                    (tipo, nombre_param)
                )

        self.functions[nombre] = {
            "params": parametros,
            "block": ctx.bloque()
        }

    def visitLlamadaFuncion(self, ctx):
        nombre = ctx.ID().getText()
        if nombre not in self.functions:
            raise Exception(f"Función {nombre} no definida")

        funcion = self.functions[nombre]

        argumentos = []
        if ctx.argumentos():
            for expr in ctx.argumentos().expr():
                argumentos.append(self.visit(expr))

        if len(argumentos) != len(funcion["params"]):
            raise Exception("Cantidad incorrecta de argumentos")

        old_memory = self.memory.copy()

        for (tipo,nombre),valor in zip(funcion["params"], argumentos):
            self.memory[nombre] = {
                "tipo": tipo,
                "valor": valor
            }

        self.visit(funcion["block"])
        self.memory = old_memory