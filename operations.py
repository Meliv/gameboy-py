
def nop(cpu): # 0x00 NOP
    cpu.PC += 1
    return 4

def stop(cpu): # 0x01 stop
    cpu.PC += 2
    return 4

def ld_sp_d16(cpu,mem): # 0x31 LD SP, d16
    cpu.SP = (mem[cpu.PC+2] << 8) + mem[cpu.PC+1]
    cpu.PC += 3
    return 12

def XOR_A(cpu): # 0xaf XOR A
    cpu.A ^= cpu.A
    if cpu.A == 0: cpu.F |= 1 << 7
    else: cpu.F &= ~(1 << 7) & 127
    return 4

op_codes = {
    0x00: lambda cpu: nop(cpu),
    0x01: lambda cpu: stop(cpu),
    
    0x31: lambda cpu: ld_sp_d16(cpu,cpu.M),

    0xaf: lambda cpu,_: XOR_A(cpu),
}