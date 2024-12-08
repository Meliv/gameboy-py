import operations

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

    @property
    def BC(self): return (self.B << 8) | self.C
    @BC.setter
    def BC(self, value):
        self.B = ((255 << 8) & value) >> 8
        self.C = 255 & value
    
    @property
    def DE(self): return (self.D << 8) | self.E
    @DE.setter
    def DE(self, value):
        self.D = ((255 << 8) & value) >> 8
        self.E = 255 & value
    
    @property
    def HL(self): return (self.H << 8) | self.L
    @HL.setter
    def HL(self, value):
        self.H = ((255 << 8) & value) >> 8
        self.L = 255 & value
    
    def execute_next_instruction(self) -> int:
        o = self.M[self.PC]
        cycles = operations.op_codes[o](self)
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