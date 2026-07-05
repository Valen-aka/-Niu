; ModuleID = "Ñu"
; target triple = "unknown-unknown-unknown"
; target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare double @"pow"(double %".1", double %".2")

define i32 @"main"()
{
entry:
  %"numero_limite" = alloca i32
  store i32 8, i32* %"numero_limite"
  %".3" = load i32, i32* %"numero_limite"
  %"call_num_duplicaciones" = call i32 @"num_duplicaciones"(i32 2, i32 %".3")
  %".4" = getelementptr [4 x i8], [4 x i8]* @".str.2", i32 0, i32 0
  %".5" = call i32 (i8*, ...) @"printf"(i8* %".4", i32 %"call_num_duplicaciones")
  ret i32 0
}

define i32 @"num_duplicaciones"(i32 %".1", i32 %".2")
{
entry:
  %"num_base" = alloca i32
  store i32 %".1", i32* %"num_base"
  %"limite" = alloca i32
  store i32 %".2", i32* %"limite"
  %".6" = load i32, i32* %"num_base"
  %".7" = load i32, i32* %"limite"
  %"cmp" = icmp sgt i32 %".6", %".7"
  br i1 %"cmp", label %"if.then", label %"if.end"
if.end:
  %"cont" = alloca i32
  store i32 0, i32* %"cont"
  br label %"while.cond"
if.then:
  %".9" = getelementptr [50 x i8], [50 x i8]* @".str.0", i32 0, i32 0
  %".10" = getelementptr [4 x i8], [4 x i8]* @".str.1", i32 0, i32 0
  %".11" = call i32 (i8*, ...) @"printf"(i8* %".10", i8* %".9")
  ret i32 0
while.cond:
  %".15" = load i32, i32* %"num_base"
  %".16" = load i32, i32* %"limite"
  %"cmp.1" = icmp slt i32 %".15", %".16"
  br i1 %"cmp.1", label %"while.body", label %"while.end"
while.body:
  %".18" = load i32, i32* %"num_base"
  %"tmp_mul" = mul i32 %".18", 2
  store i32 %"tmp_mul", i32* %"num_base"
  %".20" = load i32, i32* %"cont"
  %"tmp_add" = add i32 %".20", 1
  store i32 %"tmp_add", i32* %"cont"
  br label %"while.cond"
while.end:
  %".23" = load i32, i32* %"cont"
  ret i32 %".23"
}

@".str.0" = constant [50 x i8] [i8 69, i8 108, i8 32, i8 110, i8 117, i8 109, i8 101, i8 114, i8 111, i8 32, i8 98, i8 97, i8 115, i8 101, i8 32, i8 110, i8 111, i8 32, i8 100, i8 101, i8 98, i8 101, i8 32, i8 115, i8 101, i8 114, i8 32, i8 109, i8 97, i8 121, i8 111, i8 114, i8 32, i8 97, i8 108, i8 32, i8 110, i8 117, i8 109, i8 101, i8 114, i8 111, i8 32, i8 108, i8 105, i8 109, i8 105, i8 116, i8 101, i8 0]
@".str.1" = constant [4 x i8] [i8 37, i8 115, i8 10, i8 0]
@".str.2" = constant [4 x i8] [i8 37, i8 100, i8 10, i8 0]