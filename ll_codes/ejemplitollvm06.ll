; ModuleID = "Ñu"
; target triple = "unknown-unknown-unknown"
; target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare double @"pow"(double %".1", double %".2")

define i32 @"main"()
{
entry:
  %"call_suma" = call i32 @"suma"(i32 5, i32 3)
  %".2" = getelementptr [4 x i8], [4 x i8]* @".str.0", i32 0, i32 0
  %".3" = call i32 (i8*, ...) @"printf"(i8* %".2", i32 %"call_suma")
  ret i32 0
}

define i32 @"suma"(i32 %".1", i32 %".2")
{
entry:
  %"a" = alloca i32
  store i32 %".1", i32* %"a"
  %"b" = alloca i32
  store i32 %".2", i32* %"b"
  %".6" = load i32, i32* %"a"
  %".7" = load i32, i32* %"b"
  %"tmp_add" = add i32 %".6", %".7"
  ret i32 %"tmp_add"
}

@".str.0" = constant [4 x i8] [i8 37, i8 100, i8 10, i8 0]