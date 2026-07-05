; ModuleID = "Ñu"
; target triple = "unknown-unknown-unknown"
; target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare double @"pow"(double %".1", double %".2")

define i32 @"main"()
{
entry:
  %"x" = alloca i32
  store i32 0, i32* %"x"
  br label %"while.cond"
while.cond:
  %".4" = load i32, i32* %"x"
  %"cmp" = icmp slt i32 %".4", 5
  br i1 %"cmp", label %"while.body", label %"while.end"
while.body:
  %".6" = load i32, i32* %"x"
  %".7" = getelementptr [4 x i8], [4 x i8]* @".str.0", i32 0, i32 0
  %".8" = call i32 (i8*, ...) @"printf"(i8* %".7", i32 %".6")
  %".9" = load i32, i32* %"x"
  %"tmp_add" = add i32 %".9", 1
  store i32 %"tmp_add", i32* %"x"
  br label %"while.cond"
while.end:
  ret i32 0
}

@".str.0" = constant [4 x i8] [i8 37, i8 100, i8 10, i8 0]