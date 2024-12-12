def nop(cpu):                   # 0x00 NOP
    cpu.PC += 1
    return 4

def ld_bc_d16(cpu,mem):         # 0x01 LD BC, d16
    cpu.B = mem[cpu.PC+2]
    cpu.C = mem[cpu.PC+1]
    cpu.PC += 3
    return 12

def ld_bc_a(cpu,mem):           # 0x02 LD (BC), A
    mem[cpu.BC] = cpu.A
    cpu.PC += 1
    return 8

def inc_bc(cpu):                # 0x03 INC BC
    cpu.BC += 1
    cpu.PC += 1
    return 8

def inc_b(cpu):                 # 0x04 INC B
    cpu.F_Z = int(cpu.B + 1 == 0)
    cpu.F_N = 0
    cpu.F_H = int((cpu.B & 0x0f) + 1 > 0x0f)
    cpu.B += 1
    return 4

def dec_b(cpu):                 # 0x05 DEC B
    cpu.F_Z = int(cpu.B - 1 == 0)
    cpu.F_N = 1
    cpu.F_H = int((cpu.B & 0x0f) - 1 > 0xff)
    cpu.B -= 1
    return 4

def ld_b_d8(cpu,mem):           # 0x06 LD B, d8
    cpu.B = mem[cpu.PC+1]
    cpu.PC += 2
    return 8

def rlca(cpu):                  # 0x07 RLCA
    cpu.F_Z = 0
    cpu.F_N = 0
    cpu.F_H = 0
    cpu.F_C = ((cpu.A << 1) & 256) >> 8
    cpu.A = ((cpu.A << 1) & 255) | cpu.F_C
    return 4

def ld_a16_sp(cpu,mem):         # 0x08 LD a16, SP
    m_address = (mem[cpu.PC+2] << 8) | mem[cpu.PC+1]
    mem[m_address] = cpu.SP & 255
    mem[m_address+1] = (cpu.SP >> 8) & 255
    cpu.PC += 3
    return 20

def stop(cpu):                  # 0x10 stop
    # TODO - Not sure I understand what this does atm
    cpu.PC += 2
    return 4

def ld_de_d16(cpu,mem):         # 0x11 LD DE, d16
    cpu.D = mem[cpu.PC+2]
    cpu.E = mem[cpu.PC+1]
    cpu.PC += 3
    return 12

def jr_nz_r8(cpu,mem):          # 0x20 JR NZ, r8
    if cpu.F_Z:
        cpu.PC += 1
        return 8

    cpu.PC += mem[cpu.PC+1]
    return 12

def ld_hl_d16(cpu,mem):         # 0x21 LD HL, d16
    cpu.H = mem[cpu.PC+2]
    cpu.L = mem[cpu.PC+1]
    cpu.PC += 3
    return 12

def jr_nc_r8(cpu,mem):          # 0x30 JR NZ, r8
    if not cpu.F_C:
        cpu.PC += mem[cpu.PC+1]
        return 12
    
    cpu.PC += 1
    return 8

def ld_sp_d16(cpu,mem):         # 0x31 LD SP,d16
    cpu.SP = (mem[cpu.PC+2] << 8) | mem[cpu.PC+1]
    cpu.PC += 3
    return 12

def xor_a(cpu):                 # 0xaf XOR A
    cpu.A ^= cpu.A
    if cpu.A: cpu.FZ = 0
    else: cpu.F_Z = 1
    return 4