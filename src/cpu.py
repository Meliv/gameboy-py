import operations

class CPU:
    def __init__(self, memory=None):
        
        # Memory
        self.M = memory if memory is not None else [0x0] * (0xffff + 1)
        
        self._a = 0x0               # Accumulator
        self._f = 0x0               # Flags

        self._b = 0x0               # 8-bit registers
        self._c = 0x0
        self._d = 0x0
        self._e = 0x0
        self._h = 0x0
        self._l = 0x0
        
                                    # 16-bit registers
        self.SP = 0x0               # Stack Pointer
        self.PC = 0x0               # Program Counter


    @property
    def A(self): return self._a
    @A.setter
    def A(self, value): self._a = value & 0xff

    @property
    def B(self): return self._b
    @B.setter
    def B(self, value): self._b = value & 0xff
    
    @property
    def C(self): return self._c
    @C.setter
    def C(self, value): self._c = value & 0xff
    
    @property
    def D(self): return self._d
    @D.setter
    def D(self, value): self._d = value & 0xff
    
    @property
    def E(self): return self._e
    @E.setter
    def E(self, value): self._e = value & 0xff
    
    @property
    def F(self): return self._f
    @F.setter
    def F(self, value): self._f = value & 0xff
    
    @property
    def H(self): return self._h
    @H.setter
    def H(self, value): self._h = value & 0xff
    
    @property
    def L(self): return self._l
    @L.setter
    def L(self, value): self._l = value & 0xff

    @property
    def BC(self): return (self._b << 8) | self._c
    @BC.setter
    def BC(self, value):
        self._b = ((255 << 8) & value) >> 8
        self._c = 255 & value
    
    @property
    def DE(self): return (self._d << 8) | self._e
    @DE.setter
    def DE(self, value):
        self._d = ((255 << 8) & value) >> 8
        self._e = 255 & value
    
    @property
    def HL(self): return (self._h << 8) | self._l
    @HL.setter
    def HL(self, value):
        self._h = ((255 << 8) & value) >> 8
        self._l = 255 & value
    
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