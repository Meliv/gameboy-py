
def nop(): # 0x00 NOP
    return 1

def ld_sp_d16(cpu,mem): # 0x31 LD SP, d16
    cpu.SP = (mem[cpu.PC+2] << 8) + mem[cpu.PC+1]
    cpu.PC += 3
    return 3

def XOR_A(cpu): # 0xaf XOR A
    cpu.A ^= cpu.A
    if cpu.A == 0: cpu.F |= 1 << 7
    else: cpu.F &= ~(1 << 7) & 127
    return 1

op_codes = {
    0x00: lambda _: nop(),
    
    0x31: lambda cpu,mem: ld_sp_d16(cpu,mem),

    0xaf: lambda cpu,_: XOR_A(cpu),
}