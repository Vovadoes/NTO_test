lst = [0xaa, 0xfa, 0x01]

for i in lst:
    print(i.to_bytes(1, 'big'))