from . import operations

def process(c, cpu):
    codes = {
        0x00: lambda cpu: operations.nop(cpu),
        0x01: lambda cpu: operations.ld_bc_d16(cpu, cpu.M),
        0x02: lambda cpu: operations.ld_bc_a(cpu, cpu.M),
        0x03: lambda cpu: operations.inc_bc(cpu),
        0x04: lambda cpu: operations.inc_b(cpu),    
        0x05: lambda cpu: operations.dec_b(cpu),
        0x06: lambda cpu: operations.ld_b_d8(cpu, cpu.M),
        0x07: lambda cpu: operations.rlca(cpu),
        0x08: lambda cpu: operations.ld_a16_sp(cpu),
        0x09: lambda cpu: operations.add_hl_bc(cpu),
        
        0x10: lambda cpu: operations.stop(cpu),
        0x11: lambda cpu: operations.ld_de_d16(cpu,cpu.M),
        
        0x20: lambda cpu: operations.jr_nz_r8(cpu,cpu.M),
        0x21: lambda cpu: operations.ld_hl_d16(cpu,cpu.M),
        
        0x30: lambda cpu: operations.jr_nc_r8(cpu,cpu.M),
        0x31: lambda cpu: operations.ld_sp_d16(cpu,cpu.M),

        0xaf: lambda cpu: operations.xor_a(cpu),
    }
        
    return codes[c](cpu)