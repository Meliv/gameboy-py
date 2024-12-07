# Tidy this up later

boot_rom = []

boot_rom[0x0] = 0x31 # LD SP,$fffe
boot_rom[0x1] = 0xfe 
boot_rom[0x2] = 0xff
boot_rom[0x3] = 0xaf # XOR A 




# 0x01
#LD BC, d16
#00 00 0001

# 0x11
#LD DE, d16
#00 01 0001

# 0x21
#LD HL, d16
#00 10 0001

# 0x31
#LD SP, d16
#00 11 0001