; ModuleID = "Ñu"
; target triple = "unknown-unknown-unknown"
; target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

define i32 @"main"()
{
entry:
  %"x" = alloca i32
  store i32 10, i32* %"x"
  %"y" = alloca i32
  store i32 20, i32* %"y"
  %".4" = load i32, i32* %"x"
  %".5" = load i32, i32* %"y"
  %"tmp_add" = add i32 %".4", %".5"
  %"z" = alloca i32
  store i32 %"tmp_add", i32* %"z"
  ret i32 0
}
