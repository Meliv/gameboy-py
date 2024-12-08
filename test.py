a = 0xff - 29
print(f"a = {a:016b}")

b = 0xff - 109
print(f"b = {b:016b}")

c = a << 8
print(f"c = {c:016b}")

d = b | c
print(f"m = {d:016b}")