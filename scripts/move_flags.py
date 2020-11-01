import csv

moves = []

with open("../db/data/moves.csv", encoding="utf8", errors='ignore') as infile:
    reader = csv.reader(infile)
    header = next(reader, None)
        for row in reader:
            for i in range(8, 25):
                if i == 23:
                    pass
                else:
                    if row[i] == "True":
                        outfile.write(row[0] + ',' + str(i - (8 if i != 24 else 9)) + "\n")
