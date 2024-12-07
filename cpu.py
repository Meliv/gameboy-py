from operations import op_codes

class CPU:
    def __init__(self):
        self.M = [0x0] * 0xffff # Memory
        
        self.A = 0x0            # Accumulator
        self.F = 0x0            # Flags

        self.B = 0x0            # 8-bit registers
        self.C = 0x0
        self.D = 0x0
        self.E = 0x0
        self.H = 0x0
        self.L = 0x0
        
                                # 16-bit registers
        self.SP = 0x0           # Stack Pointer
        self.PC = 0x0           # Program Counter

    def execute_next_instruction(self):
        o = self.M[self.PC]
        cycles = op_codes[o](self)
        return cycles
    
    def start(self):
        
        # 4194304 cycles per second (4.194304 MHz)
        # 60 fps = 4194304/60 = 69905 (0.069905MHz)
        # Every 69905 cycles, refresh
        
        MAX_CYCLES, cycles = 69905, 0
    
        while cycles < MAX_CYCLES:
            c = self.execute_next_instruction()
            cycles += c


        # Update graphics etc here
        pass
