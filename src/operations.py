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
    if cpu.F & (1 << 4):
        cpu.PC += 1
        return 8

    cpu.PC += mem[cpu.PC+1]
    return 12

def ld_sp_d16(cpu,mem):         # 0x31 LD SP,d16
    cpu.SP = (mem[cpu.PC+2] << 8) + mem[cpu.PC+1]
    cpu.PC += 3
    return 12

def XOR_A(cpu):                 # 0xaf XOR A
    cpu.A ^= cpu.A
    if cpu.A: cpu.F |= 1 << 7
    else: cpu.F &= ~(1 << 7) & 127
    return 4

op_codes = {
    0x00: lambda cpu: nop(cpu),
    0x01: lambda cpu: ld_bc_d16(cpu,cpu.M),
    0x02: lambda cpu: ld_bc_a(cpu, cpu.M),
    0x03: lambda cpu: inc_bc(cpu),
    
    0x10: lambda cpu: stop(cpu),
    0x11: lambda cpu: ld_de_d16(cpu,cpu.M),
    
    0x20: lambda cpu: jr_nz_r8(cpu,cpu.M),
    0x21: lambda cpu: ld_hl_d16(cpu,cpu.M),
    
    0x30: lambda cpu: jr_nc_r8(cpu,cpu.M),
    0x31: lambda cpu: ld_sp_d16(cpu,cpu.M),

    0xaf: lambda cpu: XOR_A(cpu),
}