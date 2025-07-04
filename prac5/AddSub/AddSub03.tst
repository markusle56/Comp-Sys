load AddSub.asm,
output-file AddSub03.out,
compare-to AddSub03.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2 RAM[3]%D2.6.2;


set PC 0,
set RAM[0] 0,  // Set R0
set RAM[1] 100,  // Set R1
set RAM[2] -50,  // Set R2
set RAM[3] 40;  // Set R3
repeat 100 {
  ticktock;    // Run for 100 clock cycles
}
set RAM[1] 100,  // Restore arguments in case program used them
set RAM[2] -50,
set RAM[3] 40,
output;        // Output to file
