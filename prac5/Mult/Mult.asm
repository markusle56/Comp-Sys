// This file is based on part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: Mult.asm

// Multiplies R1 and R2 and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@R0
M=0

@R1
D=M
@R3
M=D
@END
D; JEQ

@R2
D=M
@R4
M=D
@END
D; JEQ

@R5
M=0

@R6
M=0
@R1
D=M
@SKIP_1
D; JGT
@R6
M=1
@R3
M=-M

(SKIP_1)
@R7
M=0
@R2
D=M
@SKIP_2
D; JGT
@R7
M=1
@R4
M=-M
(SKIP_2)

(LOOP)
@R4
D=M
@R5
M=M+D
@R3
M=M-1
D=M
@LOOP
D;JGT

@R6
D=M
@R7
D=D-M
@POS
D; JEQ
@R5
M=-M

(POS)
@R5
D=M
@R0
M=D

(END)
@END
0;JMP

