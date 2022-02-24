from pprint import *

x = [-9, -8, -7, -1, 1, 7, 8, 9]

result = []

for i in range(64):
    row = i // 8
    col = i % 8
    targets = {-9, -8, -7, -1, 1, 7, 8, 9}
    if col == 0:
        targets -= {-9, -1, 7}
    elif col == 7:
        targets -= {-7, 1, 9}
    if row == 0:
        targets -= {-9, -8, -7}
    elif row == 7:
        targets -= {7, 8, 9}
    result.append([i + j for j in targets])

print(result)

# counter = 0
# for i in result:
#     print(counter)
#     for rank in range(8):
#         for file in range(8):
#             if file == 0:
#                 print()
#                 print(f"{8 - rank}    ", end="")
#             if rank * 8 + file in i:
#                 print("1 ", end="")
#             else:
#                 print(". ", end="")
#     print()
#     print()
#     print("     a b c d e f g h")
#     print()
#     print()
#     counter += 1
