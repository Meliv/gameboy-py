from processor.cpu import CPU

 # Debug. Fill up memory with NOP instructions
cpu = CPU()

with open(f"etc/roms/bootrom.bin", "rb") as f:
        for i,b in enumerate(f.read()):
            cpu.M[i] = b
            print(f'b = {b:08b} {hex(b)} {b}')  

cpu.start()

print('Completed')