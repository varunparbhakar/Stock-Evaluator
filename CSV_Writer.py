import csv
class WRITE_CSV:
    def __init__(self):










stockisThere = False
stockDataRead = open("test.csv", "r")
csv_reader = list(csv.reader(stockDataRead))
#

for line in csv_reader:
    print(line)

print("Checking for changes")

for line in csv_reader:
    if(line[0] == "jesus"):
       line[0] = "Varun"
       print()
       print()
       print("CHANGE HAS BEEN MADE")
       print(line)
       print()
       print()

for line in csv_reader:
    print(line)
stockDataRead.close()
print(int(csv_reader[0][0]))
stockDataWrite = open("test.csv", "w", newline='')
csv_writer = csv.writer(stockDataWrite)
csv_writer.writerow(csv_reader[0])
csv_writer.writerow(csv_reader[1])

