print('Set Z bit to 1')
r = 0                   # 00000000
m = 1<<7                # 10000000
print(f'r = {r:08b}')
print(f'm = {m:08b}')
r |= m               # 10000000
print(f'r = {r:08b}')


print(hex(r))


print('Set Z bit to 0')
m = ~(1 << 7) & 127     # 01111111

print(f'r = {r:08b}')
print(f'm = {m:08b}')
r &= m               # 00000000
print(f'r = {r:08b}')
print(hex(r))

