def NOP_00(): return 1

def LD_B_B_40(cpu): cpu.B += 1; return 1

op_codes = {
    0x00: lambda x: NOP_00(),
    0x40: lambda x: LD_B_B_40(x),
    0x41: lambda x: LD_B_B_40(x),
}