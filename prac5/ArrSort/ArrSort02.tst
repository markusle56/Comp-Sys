// Sample Test file for ArrSort.asm
// Follows the Test Scripting Language format described in 
// Appendix B of the book "The Elements of Computing Systems"

load ArrSort.asm,
output-file ArrSort02.out,
compare-to ArrSort02.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2 RAM[40]%D2.6.2 RAM[41]%D2.6.2 RAM[42]%D2.6.2 RAM[43]%D2.6.2;

set PC 0,
set RAM[0]  0,  // Set R0
set RAM[1]  40, // Set R1
set RAM[2]  4,  // Set R2
set RAM[40] -32768,  // Set Arr[0]
set RAM[41] 342,  // Set Arr[1]
set RAM[42] 2,  // Set Arr[2]
set RAM[43] 1;  // Set Arr[3]
repeat 600 {
  ticktock;    // Run for 600 clock cycles
}
set RAM[1] 40,  // Restore arguments in case program used them
set RAM[2] 4,
output;        // Output to file

