from operations import op_codes

class CPU():
        
    # Registers

    # 8-bit

    # Accumulator
    A: int = 0x0

    # Flags
    F: int = 0x0

    B: int = 0x0
    C: int = 0x0
    D: int = 0x0
    E: int = 0x0
    H: int = 0x0
    L: int = 0x0


    # 16-bit

    # Stack Pointer
    SP: int = 0x0

    # Program Counter
    PC: int = 0x0
    
    
    # Memory
    
    M: list[int] = []

    # Operations

    def __ExecuteNextInstruction__(self):
        cycles = op_codes[self.M[self.PC]](self)
        self.PC += 1
        return cycles
    
    def Run(self):
        
        # 4194304 cycles per second (4.194304 MHz)
        # 60 fps = 4194304/60 = 69905 (0.069905MHz)
        # Every 69905 cycles, refresh
        
        MAX_CYCLES, cycles = 69905, 0
    
        while cycles < MAX_CYCLES:
            c = self.__ExecuteNextInstruction__()
            cycles += c


        # Update graphics etc here
        pass
