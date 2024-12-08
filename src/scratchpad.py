'''a = 27593
print(f"a = {a:016b} {len(format(f'{a:016b}'))}-bit = {a}")

h = ((255 << 8) & a) >> 8
print(f"h = {h:016b} {len(format(f'{h:016b}'))}-bit = {h}")

l = 255 & a
print(f"l = {l:016b} {len(format(f'{l:016b}'))}-bit = {l}")'''


h = 65535
print(f"h = {h:016b} {len(format(f'{h:016b}'))}-bit = {h}")

h = 255
print(f"h = {h:016b} {len(format(f'{h:016b}'))}-bit = {h}")