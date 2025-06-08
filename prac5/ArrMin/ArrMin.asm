// Finds the smallest element in the array of length R2 whose first element is at RAM[R1] and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R2
D=M
@END
D;JLE


@R1
A=M
D=M
@R0
M=D

(LOOP)
@R2
M=M-1
D=M
@END
D; JLE

@R1
M=M+1
A=M 
D=M
@IS_NEG
D; JLE

@R0
A=M
D=A
@SKIP
D; JLE

(COMPARE)
@R1
A=M
D=M
@R0
D=D-M
@SKIP
D; JGT

(UPDATE)
@R1 
A=M 
D=M
@R0
M=D

(SKIP)
@LOOP
0;JMP

(END)
@END
0;JMP

(IS_NEG)
@R0
D=M
@UPDATE
D; JGT
@COMPARE
0; JMP