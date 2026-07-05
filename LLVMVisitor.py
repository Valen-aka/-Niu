from llvmlite import ir
from ñuParser import ñuParser
from ñuVisitor import ñuVisitor

INT = ir.IntType(32)
DOUBLE = ir.DoubleType()
BOOL = ir.IntType(1)
CHARPTR = ir.IntType(8).as_pointer()

class LLVMVisitor(ñuVisitor):
    def __init__(self):
        self.module = ir.Module(name="Ñu")
        self.builder = None
        self.function = None
        self.variables = {}
        self.functions = {}

        self.printf = None
        self.pow = None
        self.string_counter = 0
        self.declare_printf()
        self.declare_pow()

    # === HELPERS ===
    def llvm_type(self, tipo): # -> inferir tipo
        if tipo == "num":
            return INT

        if tipo == "bool":
            return BOOL

        if tipo == "texto":
            return CHARPTR

    def promote(self, left, right): # -> convertir tipos a un tipo comun (en caso se sume un float con un int)
        if left.type == ir.DoubleType() and right.type == ir.IntType(32):
            right = self.builder.sitofp(right, ir.DoubleType())

        elif left.type == ir.IntType(32) and right.type == ir.DoubleType():
            left = self.builder.sitofp(left, ir.DoubleType())

        return left, right

    # Para funcion mostrar()
    def declare_printf(self):
        voidptr_ty = ir.IntType(8).as_pointer()

        printf_ty = ir.FunctionType(
            ir.IntType(32),
            [voidptr_ty],
            var_arg=True
        )

        self.printf = ir.Function(
            self.module,
            printf_ty,
            name="printf"
        )

    def declare_pow(self):
        # Declarar pow(double, double) -> double de libm
        double_ty = ir.DoubleType()
        pow_ty = ir.FunctionType(double_ty, [double_ty, double_ty])
        self.pow = ir.Function(self.module, pow_ty, name="pow")

    def _register_function(self, func_ctx):
        nombre = func_ctx.ID().getText()

        # Obtener tipos de parametros
        param_types = []
        param_names = []
        if func_ctx.parametros():
            for p in func_ctx.parametros().parametro():
                tipo = p.tipo().getText()
                param_types.append(self.llvm_type(tipo))
                param_names.append(p.ID().getText())

        # Por simplicidad, retornamos i32 por defecto
        return_type = ir.IntType(32)

        # Crear tipo y funcion LLVM
        func_type = ir.FunctionType(return_type, param_types)
        func = ir.Function(self.module, func_type, name=nombre)

        # Guardar info de la funcion
        self.functions[nombre] = {
            "llvm_func": func,
            "params": list(zip(
                [p.tipo().getText() for p in func_ctx.parametros().parametro()] if func_ctx.parametros() else [],
                param_names
            )),
            "block": func_ctx.bloque()
        }

    # Genera la funcion main de IR:
    # define i32 @main(){}
    def visitRoot(self, ctx):
        main_type = ir.FunctionType(
            ir.IntType(32),
            []
        )

        self.function = ir.Function(
            self.module,
            main_type,
            "main"
        )

        block = self.function.append_basic_block("entry")
        self.builder = ir.IRBuilder(block)

        # Primera pasada: registrar firmas de funciones
        for stmt in ctx.stat():
            if hasattr(stmt, 'funcionStat') and stmt.funcionStat() is not None:
                self._register_function(stmt.funcionStat())

        # Segunda pasada: generar codigo
        for stmt in ctx.stat():
            self.visit(stmt)

        self.builder.ret(ir.Constant(ir.IntType(32), 0))
        return self.module
    
    # === Declaraciones y asignaciones ===
    def visitDeclaracion(self, ctx):
        nombre = ctx.ID().getText()
        valor = self.visit(ctx.expr())

        ptr = self.builder.alloca(
            valor.type,
            name=nombre
        )

        self.builder.store(valor, ptr)
        self.variables[nombre] = ptr

        return valor

    def visitAsignacion(self, ctx):
        nombre = ctx.ID().getText()
        valor = self.visit(ctx.expr())
        ptr = self.variables[nombre]

        self.builder.store(valor, ptr)
        return valor
    
    def visitVariable(self, ctx):
        nombre = ctx.getText()
        ptr = self.variables[nombre]

        return self.builder.load(ptr)
    
    def visitNumero(self, ctx):
        texto = ctx.getText()

        if "." in texto:

            return ir.Constant(
                ir.DoubleType(),
                float(texto)
            )

        return ir.Constant(
            ir.IntType(32),
            int(texto)
        )

    def visitBooleano(self,ctx):
        if ctx.getText()=="verdadero":
            return ir.Constant(ir.IntType(1),1)

        return ir.Constant(ir.IntType(1),0)

    def visitNegativo(self, ctx):
        valor = self.visit(ctx.atom())
        cero = ir.Constant(valor.type,0)

        return self.builder.sub(cero, valor)

    def visitParentesis(self, ctx):
        return self.visit(ctx.expr())
    
    # === Operaciones matematicas y comparaciones ===
    def visitAddSub(self, ctx):
        left = self.visit(ctx.addExpr())
        right = self.visit(ctx.mulExpr())

        op_type = ctx.op.type

        if op_type == ñuParser.MAS:
            return self.builder.add(left, right, name="tmp_add")
        elif op_type == ñuParser.MENOS:
            return self.builder.sub(left, right, name="tmp_sub")
        
    def visitMulDiv(self, ctx):
        left = self.visit(ctx.mulExpr())
        right = self.visit(ctx.powExpr())

        op_type = ctx.op.type

        if op_type == ñuParser.MULT:
            return self.builder.mul(left, right, name="tmp_mul")
        elif op_type == ñuParser.DIV:
            return self.builder.sdiv(left, right, name="tmp_div")

    def visitComparador(self, ctx):
        if ctx.op is None:
            return self.visit(ctx.addExpr(0))

        left = self.visit(ctx.addExpr(0))
        right = self.visit(ctx.addExpr(1))

        op = ctx.op.text
        return self.builder.icmp_signed(op, left, right, "cmp")

    # === WRAPPERS (stat) ===
    def visitToDeclaracion(self, ctx):
        return self.visit(ctx.declaracion())

    def visitToAsignacion(self, ctx):
        return self.visit(ctx.asignacion())

    def visitPrint(self, ctx):
        return self.visit(ctx.mostrarStat())

    def visitToIf(self, ctx):
        return self.visit(ctx.ifStat())

    def visitToWhile(self, ctx):
        return self.visit(ctx.whileStat())

    def visitToFor(self, ctx):
        return self.visit(ctx.forStat())

    def visitToFuncion(self, ctx):
        return self.visit(ctx.funcionStat())

    def visitToReturn(self, ctx):
        return self.visit(ctx.returnStat())

    def visitExprStat(self, ctx):
        return self.visit(ctx.expr())

    # === WRAPPERS (expr) ===
    def visitToMul(self, ctx):
        return self.visit(ctx.mulExpr())

    def visitToPow(self, ctx):
        return self.visit(ctx.powExpr())

    def visitToAtom(self, ctx):
        return self.visit(ctx.atom())

    # === TEXT ===
    def visitTexto(self, ctx):
        texto = ctx.getText()[1:-1]
        return self._create_global_string(texto)

    def _create_global_string(self, text):
        text_with_null = text + chr(0)
        string_val = ir.Constant(
            ir.ArrayType(ir.IntType(8), len(text_with_null)),
            [ord(c) for c in text_with_null]
        )
        global_str = ir.GlobalVariable(self.module, string_val.type, name=f".str.{self.string_counter}")
        self.string_counter += 1
        global_str.initializer = string_val
        global_str.global_constant = True
        return self.builder.gep(global_str, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])

    # === PRINT (mostrar) ===
    def visitMostrarStat(self, ctx):
        valor = self.visit(ctx.expr())

        if valor.type == ir.IntType(32):
            fmt = self._create_global_string("%d\n")
            self.builder.call(self.printf, [fmt, valor])
        elif valor.type == ir.DoubleType():
            fmt = self._create_global_string("%f\n")
            self.builder.call(self.printf, [fmt, valor])
        elif valor.type == ir.IntType(1):
            extended = self.builder.zext(valor, ir.IntType(32))
            fmt = self._create_global_string("%d\n")
            self.builder.call(self.printf, [fmt, extended])
        elif valor.type == ir.IntType(8).as_pointer():
            fmt = self._create_global_string("%s\n")
            self.builder.call(self.printf, [fmt, valor])

        return valor

    # === IF ===
    def visitCondition(self, ctx):
        l = list(ctx.getChildren())

        branches = []
        has_else = False
        else_block = None
        i = 0
        while i < len(l):
            token = l[i].getText() if hasattr(l[i], 'getText') else ''
            if token == 'si':
                branches.append((l[i+1], l[i+2]))
                i += 3
            elif token == 'osino':
                branches.append((l[i+1], l[i+2]))
                i += 3
            elif token == 'sino':
                has_else = True
                else_block = l[i+1]
                i += 2
            else:
                i += 1

        end_bb = self.function.append_basic_block("if.end")

        if has_else:
            else_bb = self.function.append_basic_block("if.else")

        cond = self.visit(branches[0][0])
        then_bb = self.function.append_basic_block("if.then")

        if len(branches) == 1 and has_else:
            self.builder.cbranch(cond, then_bb, else_bb)
        elif len(branches) == 1:
            self.builder.cbranch(cond, then_bb, end_bb)
        else:
            next_bb = self.function.append_basic_block("if.elif")
            self.builder.cbranch(cond, then_bb, next_bb)

        self.builder.position_at_end(then_bb)
        self.visit(branches[0][1])
        if not self.builder.block.is_terminated:
            self.builder.branch(end_bb)

        for idx in range(1, len(branches)):
            self.builder.position_at_end(next_bb)
            cond = self.visit(branches[idx][0])

            then_bb = self.function.append_basic_block(f"if.then.{idx}")

            if idx == len(branches) - 1 and has_else:
                self.builder.cbranch(cond, then_bb, else_bb)
            elif idx == len(branches) - 1:
                self.builder.cbranch(cond, then_bb, end_bb)
            else:
                next_bb = self.function.append_basic_block(f"if.elif.{idx}")
                self.builder.cbranch(cond, then_bb, next_bb)

            self.builder.position_at_end(then_bb)
            self.visit(branches[idx][1])
            if not self.builder.block.is_terminated:
                self.builder.branch(end_bb)

        if has_else:
            self.builder.position_at_end(else_bb)
            self.visit(else_block)
            if not self.builder.block.is_terminated:
                self.builder.branch(end_bb)

        self.builder.position_at_end(end_bb)

    # === WHILE ===
    def visitWhile(self, ctx):
        l = list(ctx.getChildren())

        cond_bb = self.function.append_basic_block("while.cond")
        body_bb = self.function.append_basic_block("while.body")
        end_bb = self.function.append_basic_block("while.end")

        self.builder.branch(cond_bb)

        self.builder.position_at_end(cond_bb)
        cond = self.visit(l[1])
        self.builder.cbranch(cond, body_bb, end_bb)

        self.builder.position_at_end(body_bb)
        self.visit(l[2])
        if not self.builder.block.is_terminated:
            self.builder.branch(cond_bb)

        self.builder.position_at_end(end_bb)

    # === FOR ===
    def visitFor(self, ctx):
        l = list(ctx.getChildren())

        self.visit(l[2])

        cond_bb = self.function.append_basic_block("for.cond")
        body_bb = self.function.append_basic_block("for.body")
        end_bb = self.function.append_basic_block("for.end")

        self.builder.branch(cond_bb)

        self.builder.position_at_end(cond_bb)
        cond = self.visit(l[4])
        self.builder.cbranch(cond, body_bb, end_bb)

        self.builder.position_at_end(body_bb)
        self.visit(l[8])
        self.visit(l[6])
        if not self.builder.block.is_terminated:
            self.builder.branch(cond_bb)

        self.builder.position_at_end(end_bb)

    # === FOR HELPERS ===
    def visitInitDeclaracion(self, ctx):
        return self.visit(ctx.declaracion())

    def visitInitAsignacion(self, ctx):
        return self.visit(ctx.asignacion())

    def visitUpdateAsignacion(self, ctx):
        return self.visit(ctx.asignacion())

    # === POWER ===
    def visitPotencia(self, ctx):
        base = self.visit(ctx.atom())
        exponent = self.visit(ctx.powExpr())

        # pow() de C trabaja con doubles, convertir ambos operandos
        if base.type == ir.IntType(32):
            base = self.builder.sitofp(base, ir.DoubleType())
        if exponent.type == ir.IntType(32):
            exponent = self.builder.sitofp(exponent, ir.DoubleType())

        resultado = self.builder.call(self.pow, [base, exponent], name="call_pow")

        return resultado

    # === FUNCIONES ===
    def visitFuncion(self, ctx):
        nombre = ctx.ID().getText()
        func_info = self.functions[nombre]
        llvm_func = func_info["llvm_func"]

        # Crear bloque de entrada
        entry = llvm_func.append_basic_block("entry")

        # Guardar contexto actual de main
        old_function = self.function
        old_builder = self.builder
        old_variables = self.variables.copy()

        # Nuevo contexto para la funcion
        self.function = llvm_func
        self.builder = ir.IRBuilder(entry)
        self.variables = {}

        # Vincular parametros
        if ctx.parametros():
            for i, p in enumerate(ctx.parametros().parametro()):
                nombre_param = p.ID().getText()
                tipo = p.tipo().getText()
                ptr = self.builder.alloca(self.llvm_type(tipo), name=nombre_param)
                self.builder.store(llvm_func.args[i], ptr)
                self.variables[nombre_param] = ptr

        # Visitar cuerpo de la funcion
        self.visit(ctx.bloque())

        # Si no termino con ret, agregar ret por defecto
        if not self.builder.block.is_terminated:
            self.builder.ret(ir.Constant(ir.IntType(32), 0))

        # Restaurar contexto de main
        self.function = old_function
        self.builder = old_builder
        self.variables = old_variables

    def visitAtomFuncion(self, ctx):
        llamada = ctx.llamadaFuncion()
        nombre = llamada.ID().getText()

        if nombre not in self.functions:
            raise Exception(f"Funcion '{nombre}' no definida")

        llvm_func = self.functions[nombre]["llvm_func"]

        # Evaluar argumentos
        args = []
        if llamada.argumentos():
            for expr in llamada.argumentos().expr():
                args.append(self.visit(expr))

        # Llamar a la funcion
        return self.builder.call(llvm_func, args, name=f"call_{nombre}")

    def visitReturn(self, ctx):
        if ctx.expr():
            valor = self.visit(ctx.expr())
            self.builder.ret(valor)
        else:
            self.builder.ret(ir.Constant(ir.IntType(32), 0))
