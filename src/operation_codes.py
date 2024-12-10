import operations

ops = {
    0x00: lambda cpu: operations.nop(cpu),
    0x01: lambda cpu: operations.ld_bc_d16(cpu,cpu.M),
    0x02: lambda cpu: operations.ld_bc_a(cpu, cpu.M),
    0x03: lambda cpu: operations.inc_bc(cpu),
    
    0x10: lambda cpu: operations.stop(cpu),
    0x11: lambda cpu: operations.ld_de_d16(cpu,cpu.M),
    
    0x20: lambda cpu: operations.jr_nz_r8(cpu,cpu.M),
    0x21: lambda cpu: operations.ld_hl_d16(cpu,cpu.M),
    
    0x30: lambda cpu: operations.jr_nc_r8(cpu,cpu.M),
    0x31: lambda cpu: operations.ld_sp_d16(cpu,cpu.M),

    0xaf: lambda cpu: operations.xor_a(cpu),
}