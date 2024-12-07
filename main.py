from cpu import CPU

program = [
    0x40,
    0x41,
]

 # Debug. Fill up memory with NOP instructions
for i in range(69905):
    program.append(0x00)

cpu = CPU()

cpu.M = program

cpu.Run()

print(cpu.B)