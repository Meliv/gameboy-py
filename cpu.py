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
    
    O = {
        0x00: lambda x: x.__NOP_00__(),
        0x40: lambda x: x.__LD_B_B_40__(),
        0x41: lambda x: x.__LD_B_B_40__(),
        0xff: lambda x: x.EXIT()
    }
    
    X = True
    
    def __NOP_00__(_): return 1
    
    def EXIT(self): self.X = False; return 0

    def __LD_B_B_40__(self): self.B += 1; return 1
    
    def __ExecuteNextInstruction__(self):
        
        memory_v = self.M[self.PC]
        
        func = self.O[memory_v]
        
        cycles = func(self)
        
        '''
        cycles = self.O[self.M[self.PC]](self)
        '''
        self.PC += 1
        
        return cycles
    
    def Run(self):
        
        while self.X:

            # 4194304 cycles per second (4.194304 MHz)
            # 60 fps = 4194304/60 = 69905 (0.069905MHz)
            # Every 69905 cycles, refresh
            
            MAX_CYCLES, cycles = 69905, 0
        
            while cycles < MAX_CYCLES:
                c = self.__ExecuteNextInstruction__()
                cycles += c


            # Update graphics etc here
            pass

program = [
    0x40,
    0x41,
    0xff
]

 # Debug. Fill up memory with NOP instructions
for i in range(69905):
    program.append(0x00)

x = CPU()

x.M = program

x.Run()

print(x.B)
 
