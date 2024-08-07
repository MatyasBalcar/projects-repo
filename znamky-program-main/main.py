import csv
from unicodedata import name
#stock code
f = open('./log.csv', 'w')
writer = csv.writer(f)
writer.writerow(["jmeno","id","stitek"])

#input function
def get_data():
    name_of_place = input("Jak se jmenuje misto na znamce: ")
    id_number = input("Cislo na znamce: ")
    stitek =input("je ke znamce stitek: ")
    return [name_of_place,id_number,stitek]
#*start cycle
while True:
    data = get_data()

    writer.writerow(data)

    IsContinue=input("chcete zadat dalsi znamky: ")
    if IsContinue=="n":
        break
    else:pass
f.close()