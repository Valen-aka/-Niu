; ModuleID = "Ñu"
; target triple = "unknown-unknown-unknown"
; target datalayout = ""

declare i32 @"printf"(i8* %".1", ...)

declare double @"pow"(double %".1", double %".2")

define i32 @"main"()
{
entry:
  %"edad" = alloca i32
  store i32 19, i32* %"edad"
  %".3" = load i32, i32* %"edad"
  %"cmp" = icmp sgt i32 %".3", 18
  br i1 %"cmp", label %"if.then", label %"if.elif"
if.end:
  ret i32 0
if.else:
  %".15" = getelementptr [17 x i8], [17 x i8]* @".str.4", i32 0, i32 0
  %".16" = getelementptr [4 x i8], [4 x i8]* @".str.5", i32 0, i32 0
  %".17" = call i32 (i8*, ...) @"printf"(i8* %".16", i8* %".15")
  br label %"if.end"
if.then:
  %".5" = getelementptr [14 x i8], [14 x i8]* @".str.0", i32 0, i32 0
  %".6" = getelementptr [4 x i8], [4 x i8]* @".str.1", i32 0, i32 0
  %".7" = call i32 (i8*, ...) @"printf"(i8* %".6", i8* %".5")
  br label %"if.end"
if.elif:
  %".9" = load i32, i32* %"edad"
  %"cmp.1" = icmp eq i32 %".9", 18
  br i1 %"cmp.1", label %"if.then.1", label %"if.else"
if.then.1:
  %".11" = getelementptr [12 x i8], [12 x i8]* @".str.2", i32 0, i32 0
  %".12" = getelementptr [4 x i8], [4 x i8]* @".str.3", i32 0, i32 0
  %".13" = call i32 (i8*, ...) @"printf"(i8* %".12", i8* %".11")
  br label %"if.end"
}

@".str.0" = constant [14 x i8] [i8 77, i8 97, i8 121, i8 111, i8 114, i8 32, i8 100, i8 101, i8 32, i8 101, i8 100, i8 97, i8 100, i8 0]
@".str.1" = constant [4 x i8] [i8 37, i8 115, i8 10, i8 0]
@".str.2" = constant [12 x i8] [i8 69, i8 115, i8 32, i8 49, i8 56, i8 32, i8 106, i8 117, i8 115, i8 116, i8 111, i8 0]
@".str.3" = constant [4 x i8] [i8 37, i8 115, i8 10, i8 0]
@".str.4" = constant [17 x i8] [i8 69, i8 115, i8 32, i8 109, i8 101, i8 110, i8 111, i8 114, i8 32, i8 100, i8 101, i8 32, i8 101, i8 100, i8 97, i8 100, i8 0]
@".str.5" = constant [4 x i8] [i8 37, i8 115, i8 10, i8 0]