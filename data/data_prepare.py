import csv

filename = "/home/asimsys/Desktop/Project/Kanjimnemonics/backup.csv"

newfile = open('/home/asimsys/Desktop/Project/Kanjimnemonics/new.csv', 'w')
csvfile = open(filename, 'r')

csvreader = csv.reader(csvfile)
csvwriter = csv.writer(newfile)
next(csvreader)
# csvwriter = csv.writer(csvfile)
count = 0
for row in csvreader:
    unicode = ord(list(row)[1])
    # row.append(unicode)
    # print(row)
    csvwriter.writerow([count, unicode, row[4]])
    count += 1

newfile.close()
csvfile.close()
