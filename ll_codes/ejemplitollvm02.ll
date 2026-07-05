; ModuleID = "Ñu"
; target triple = "unknown-unknown-unknown"
; target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare double @"pow"(double %".1", double %".2")

define i32 @"main"()
{
entry:
  %".2" = sitofp i32 2 to double
  %".3" = sitofp i32 3 to double
  %"call_pow" = call double @"pow"(double %".2", double %".3")
  %"x" = alloca double
  store double %"call_pow", double* %"x"
  %".5" = load double, double* %"x"
  %".6" = getelementptr [4 x i8], [4 x i8]* @".str.0", i32 0, i32 0
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6", double %".5")
  ret i32 0
}

@".str.0" = constant [4 x i8] [i8 37, i8 102, i8 10, i8 0]