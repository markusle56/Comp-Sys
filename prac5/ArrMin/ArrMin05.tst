// Sample Test file for ArrMin.asm
// Follows the Test Scripting Language format described in 
// Appendix B of the book "The Elements of Computing Systems"

load ArrMin.asm,
output-file ArrMin05.out,
compare-to ArrMin05.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2 RAM[7]%D2.6.2 RAM[8]%D2.6.2 RAM[9]%D2.6.2;

set PC 0,
set RAM[0]  0,  // Set R0
set RAM[1]  7, // Set R1
set RAM[2]  3,  // Set R2
set RAM[7] 30000,  // Set Arr[0]
set RAM[8] -32768,  // Set Arr[1]
set RAM[9] 32700,  // Set Arr[2]
repeat 300 {
  ticktock;    // Run for 300 clock cycles
}
set RAM[1] 7,  // Restore arguments in case program used them
set RAM[2] 3,
output;        // Output to file

