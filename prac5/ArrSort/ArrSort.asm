// Sorts the array of length R2 whose first element is at RAM[R1] in ascending order in place. Sets R0 to True (-1) when complete.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R2
D=M
@END
D; JLE

@R1
D=M
@R2
D=D+M
@R5
M=D

@R1
D=M
@R4
M=D-1

(OUTTER_LOOP)
@R5
D=M
@R4
D=D-M
@END
D; JLE

@R4
M=M+1
D=M
@R3
M=D

(INNER_LOOP)
@R3
M=M+1

@R5
D=M
@R3
D=D-M
@OUTTER_LOOP
D; JLE

@R3
A=M
D=M
@IS_NEG
D; JLT

@R4
A=M
D=M
@SKIP
D; JLT

(COMPARE)
@R3
A=M
D=M
@R4
A=M
D=D-M
@SKIP
D; JGE

(UPDATE)
@R3
A=M
D=M
@R0
M=D
@R4
A=M
D=M
@R3
A=M
M=D
@R0
D=M
@R4
A=M
M=D

(SKIP)
@INNER_LOOP
0; JMP


(END)
@R0
M=-1
@END
0;JMP


(IS_NEG)
@R4
A=M
D=M
@UPDATE
D; JGE
@COMPARE
0; JMP
