import csv

spamreader=csv.DictReader(open("Willy 'jiepperz' abolla/main.csv"))
jaj=list()
haya=['loudness','tempo']
list_tempo=list()
list_loudness=list()
for row in spamreader :
    list_loudness.append(float(row['loudness']))
    list_tempo.append(float(row['tempo']))
print(list_tempo)
print("max loudness=",max(list_loudness))
print("max tempo=",max(list_tempo))
print("min loudness=",min(list_loudness))
print("min tempo=",min(list_tempo))


