import csv
stockisThere = False
stockDataSpreadsheet = open("test.csv", "w")
csvWriter = csv.writer(stockDataSpreadsheet)
array = {4,5,4,6,7,8}
csvWriter.writerow(array)




csv_reader = csv.reader(stockDataSpreadsheet)
next(csv_reader) #Skiping the header
for line in csv_reader:
    print(line[0])
    if line[1] == ("apple") :
        stockisThere = True;


if stockisThere:
    print("Stock is here")

else:
    print("Not here")


