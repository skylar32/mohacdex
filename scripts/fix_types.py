import csv

types = {
         1: 1,
         2: 7,
         3: 10,
         4: 8,
         5: 9,
         6: 13,
         7: 12,
         8: 14,
         9: 17,
         10: 2,
         11: 3,
         12: 4,
         13: 5,
         14: 11,
         15: 6,
         16: 15,
         17: 16,
         18: 18
        }

moves = []
header = ""

with open("../db/data/moves.csv", 'r', errors='ignore') as infile:
    reader = csv.reader(infile)
    moves.append(next(reader, None))
    for row in reader:
        row[2] = str(types[int(row[2])])
        moves.append(row)
with open("../db/data/moves.csv", 'w') as outfile:
    for move in moves:
        outfile.write(','.join(move) + "\n")
