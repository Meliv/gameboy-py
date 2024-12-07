# For bootrom

def LD_SP_d16(cpu):
    cpu.SP = cpu.M[cpu.PC + 2] << 8 + cpu.M[cpu.PC + 1]
    cpu.PC += 3
    return 3

def XOR_A(cpu):
    cpu.A ^= cpu.A
    
    if cpu.A == 0:
        cpu.F |= 1 << 7
    else:
        cpu.F &= ~(1 << 7) & 127
    
    return 1

# End bootrom


def NOP_00(): return 1

def LD_B_B_40(cpu): cpu.B += 1; return 1

op_codes = {
    # Boot
    0x31: lambda x: LD_SP_d16(x),
    0xaf: lambda x: XOR_A(x),
    
    
    
    0x00: lambda x: NOP_00(),
    0x40: lambda x: LD_B_B_40(x),
    0x41: lambda x: LD_B_B_40(x),
}