from .cpu import CPU

# 0x00 NOP
def nop(cpu: CPU):                   
    cpu.PC += 1
    return 4

# 0x01 LD BC, d16
def ld_bc_d16(cpu: CPU, mem: list[int]):
    cpu.B = mem[cpu.PC+2]
    cpu.C = mem[cpu.PC+1]
    cpu.PC += 3
    return 12

# 0x02 LD (BC), A
def ld_bc_a(cpu: CPU, mem: list[int]):
    mem[cpu.BC] = cpu.A
    cpu.PC += 1
    return 8

# 0x03 INC BC
def inc_bc(cpu: CPU):
    cpu.BC += 1
    cpu.PC += 1
    return 8

# 0x04 INC B
def inc_b(cpu: CPU):
    cpu.F_Z = cpu.B + 1 == 0
    cpu.F_N = 0
    cpu.F_H = (cpu.B & 0x0f) + 1 > 0x0f
    cpu.B += 1
    cpu.PC += 1
    return 4

# 0x05 DEC B
def dec_b(cpu: CPU):
    cpu.F_Z = cpu.B - 1 == 0
    cpu.F_N = 1
    cpu.F_H = (cpu.B & 0x0f) - 1 > 0xff
    cpu.B -= 1
    cpu.PC += 1
    return 4

# 0x06 LD B, d8
def ld_b_d8(cpu: CPU, mem: list[int]):
    cpu.B = mem[cpu.PC+1]
    cpu.PC += 2
    return 8

# 0x07 RLCA
def rlca(cpu: CPU):
    cpu.F_Z = 0
    cpu.F_N = 0
    cpu.F_H = 0
    cpu.F_C = ((cpu.A << 1) & 256) >> 8
    cpu.A = ((cpu.A << 1) & 255) | cpu.F_C
    cpu.PC += 1
    return 4

# 0x08 LD a16, SP
def ld_a16_sp(cpu: CPU, mem: list[int]):
    m_address = (mem[cpu.PC+2] << 8) | mem[cpu.PC+1]
    mem[m_address] = cpu.SP & 255
    mem[m_address+1] = (cpu.SP >> 8) & 255
    cpu.PC += 3
    return 20

# 0x09 ADD HL, BC
def add_hl_bc(cpu: CPU):
    cpu.HL += cpu.BC
    cpu.PC += 1
    return 8

# 0x10 STOP
def stop(cpu: CPU):
    # TODO - Not sure I understand what this does atm
    cpu.PC += 2
    return 4

# 0x11 LD DE, d16
def ld_de_d16(cpu: CPU, mem: list[int]):
    cpu.D = mem[cpu.PC+2]
    cpu.E = mem[cpu.PC+1]
    cpu.PC += 3
    return 12

# 0x20 JR NZ, r8
def jr_nz_r8(cpu: CPU, mem: list[int]):
    if cpu.F_Z:
        cpu.PC += 1
        return 8

    cpu.PC += mem[cpu.PC+1]
    return 12

# 0x21 LD HL, d16
def ld_hl_d16(cpu: CPU, mem: list[int]):
    cpu.H = mem[cpu.PC+2]
    cpu.L = mem[cpu.PC+1]
    cpu.PC += 3
    return 12

# 0x30 JR NZ, r8
def jr_nc_r8(cpu: CPU, mem: list[int]):
    if not cpu.F_C:
        cpu.PC += mem[cpu.PC+1]
        return 12
    
    cpu.PC += 1
    return 8

# 0x31 LD SP,d16
def ld_sp_d16(cpu: CPU, mem: list[int]):
    cpu.SP = (mem[cpu.PC+2] << 8) | mem[cpu.PC+1]
    cpu.PC += 3
    return 12

# 0xaf XOR A
def xor_a(cpu: CPU):
    cpu.A ^= cpu.A
    if cpu.A: cpu.FZ = 0
    else: cpu.F_Z = 1
    cpu.PC += 1
    return 4