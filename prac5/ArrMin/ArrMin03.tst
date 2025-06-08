// Sample Test file for ArrMin.asm
// Follows the Test Scripting Language format described in 
// Appendix B of the book "The Elements of Computing Systems"

load ArrMin.asm,
output-file ArrMin03.out,
compare-to ArrMin03.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2 RAM[20]%D2.6.2 RAM[21]%D2.6.2 RAM[22]%D2.6.2 RAM[23]%D2.6.2 RAM[24]%D2.6.2 RAM[25]%D2.6.2 RAM[26]%D2.6.2 RAM[27]%D2.6.2 RAM[28]%D2.6.2 RAM[29]%D2.6.2 RAM[30]%D2.6.2;

set PC 0,
set RAM[0]  1,   // Arg or initial value
set RAM[1]  20,  
set RAM[2]  10,  

set RAM[20] -5,  
set RAM[21]  1,  
set RAM[22] -10, 
set RAM[23]  3,  
set RAM[24]  9,  
set RAM[25] -10, 
set RAM[26]  4,  
set RAM[27]  7,  
set RAM[28]  0,  
set RAM[29]  5,  
set RAM[30]  3;  

repeat 300 {
  ticktock;    // Run for 100 cycles
}
set RAM[1]  20,  
set RAM[2]  10,  
output;        // Write RAM[...] values to the output file
